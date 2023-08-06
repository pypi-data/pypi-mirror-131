import copy
import fnmatch
import os
import re

import numpy as np
import pandas as pd

from seeq import spy
from seeq.sdk import *
from seeq.spy import _common
from seeq.spy import _config
from seeq.spy import _login
from seeq.spy import _metadata
from seeq.spy import _push
from seeq.spy import _search
from seeq.spy._errors import *

_reference_types = ['StoredSignal', 'StoredCondition']
_calculated_types = ['CalculatedScalar', 'CalculatedSignal', 'CalculatedCondition']
_data_types = _calculated_types + _reference_types
_supported_input_types = _data_types + ['Asset']
_supported_output_types = _calculated_types + ['Asset']

_dataframe_dtypes = {
    'ID': str,
    'Referenced ID': str,
    'Path': str,
    'Name': str,
    'Type': str,
    'Depth': int,
    'Description': str,
    'Formula': str,
    'Formula Parameters': (str, list, dict, pd.Series, pd.DataFrame),
    'Cache Enabled': bool
}
_dataframe_columns = list(_dataframe_dtypes.keys())

MAX_ERRORS_DISPLAYED = 3


class Tree:
    _dataframe = pd.DataFrame()
    _workbook = _common.DEFAULT_WORKBOOK_PATH
    _workbook_id = _common.EMPTY_GUID

    quiet = False
    errors = 'raise'

    def __init__(self, data, *, friendly_name=None, description=None, workbook=_common.DEFAULT_WORKBOOK_PATH,
                 quiet=False, errors='raise', status=None):
        """
        Utilizes a Python Class-based tree to produce a set of item definitions as
        a metadata DataFrame. Allows users to manipulate the tree using various functions.

        Parameters
        ----------
        data : {pandas.DataFrame, str}
            Defines which element will be inserted at the root.
            If an existing tree already exists in Seeq, the entire tree will be pulled recursively.
            If this tree doesn't already within the scope of the workbook, new tree elements
            will be created (by deep-copy or reference if applicable).
            The following options are allowed:
            1) A name string. If an existing tree with that name (case-insensitive) is found,
                all children will be recursively pulled in.
            2) An ID string of an existing item in Seeq. If that item is in a tree, all
                children will be recursively pulled in.
            3) spy.search results or other custom dataframes. The 'Path' column must be present
                and represent a single tree structure.
            4) A filename or relative file path to a CSV file. The CSV file should have either
                a complete Name column or a complete ID column, and should specify the tree
                path for each item either in a 'Path' column formatted as "Root >> Next Level":

                +--------------------+-----------+
                | Path               | Name      |
                +--------------------+-----------+
                | Root >> Next Level | Item_Name |
                +--------------------+-----------+

                or as a series of 'Levels' columns, e.g. "Level 1" and "Level 2" columns,
                where "Level 1" would be "Root" and "Level 2" would be "Next Level":

                +---------+------------+-----------+
                | Level 1 | Level 2    | Name      |
                +---------+------------+-----------+
                | Root    | Next Level | Item_Name |
                +---------+------------+-----------+

                'Levels' columns will be forward-filled.

        friendly_name : str, optional
            Use this specified name rather than the referenced item's original name.

        description : str, optional
            The description to set on the root-level asset.

        workbook : str, default 'Data Lab >> Data Lab Analysis'
            The path to a workbook (in the form of 'Folder >> Path >> Workbook Name')
            or an ID that all pushed items will be 'scoped to'. You can
            push to the Corporate folder by using the following pattern:
            '__Corporate__ >> Folder >> Path >> Workbook Name'. A Tree currently
            may not be globally scoped. These items will not be visible/searchable
            using the data panel in other workbooks.

        quiet : bool, default False
            If True, suppresses progress output. This setting will be the default for all
            operations on this Tree. This option can be changed later using
            `tree.quiet = True` or by specifying the option for individual function calls.
            Note that when status is provided, the quiet setting of the Status object
            that is passed in takes precedent.

        errors : {'raise', 'catalog'}, default 'raise'
            If 'raise', any errors encountered will cause an exception. If 'catalog',
            errors will be added to a 'Result' column in the status.df DataFrame. The
            option chosen here will be the default for all other operations on this Tree.
            This option can be changed later using `tree.errors = 'catalog'` or by
            specifying the option for individual function calls.

        status : spy.Status, optional
            If specified, the supplied Status object will be updated as the command
            progresses. It gets filled in with the same information you would see
            in Jupyter in the blue/green/red table below your code while the
            command is executed. The table itself is accessible as a DataFrame via
            the status.df property.
        """
        _common.validate_argument_types([
            (data, 'data', (pd.DataFrame, str)),
            (friendly_name, 'friendly_name', str),
            (description, 'description', str),
            (workbook, 'workbook', str),
            (quiet, 'quiet', bool),
            (errors, 'errors', str),
            (status, 'status', _common.Status)
        ])
        _common.validate_errors_arg(errors)
        self.quiet = quiet
        self.errors = errors
        status = _common.Status.validate(status, quiet)

        self._workbook = workbook if workbook else _common.DEFAULT_WORKBOOK_PATH
        self._find_workbook_id(quiet, status)

        # check if csv file
        if isinstance(data, str):
            ext = os.path.splitext(data)[1]
            if ext == '.csv':
                # read and process csv file
                data = _process_csv_data(data, status, workbook=workbook)
                # get a path column from levels columns
                _make_paths_from_levels(data)
                # data is now a pd.DataFrame and can be handled as any df

        # If friendly_name is a column value query, we will apply it to the dataframe.
        # Otherwise, we will rename the root.
        rename_root = friendly_name is not None and \
                      not (isinstance(data, pd.DataFrame) and (_is_column_value_query(friendly_name) or len(data) == 1))

        if isinstance(data, pd.DataFrame):
            if len(data) == 0:
                raise SPyValueError("A tree may not be created from a DataFrame with no rows")

            _initialize_status_df(status, 'Created', 'Constructing Tree object from dataframe input.',
                                  _common.Status.RUNNING)

            # Check user input for errors, filter if errors='catalog'
            df = _validate_and_filter(data, status, errors, stage='input',
                                      error_message_header='Errors were encountered before creating tree',
                                      raise_if_all_filtered=True)

            df = df.reset_index(drop=True)

            # If the dataframe specifies a root with ID and Name corresponding to a previously pushed SPy tree,
            # then we want this object to modify the same tree rather than create a copy of it. If such a tree
            # exists, then we store its current state in existing_tree_df
            existing_tree_df = _get_existing_spy_tree(df, self._workbook_id)

            if friendly_name is not None:
                if _is_column_value_query(friendly_name):
                    df['Friendly Name'] = friendly_name
                elif len(df) == 1:
                    df['Name'] = friendly_name
            _apply_friendly_name(df)
            modified_items = df.modified_items

            # Sanitize data and pull in properties of items with IDs. Make items with IDs into references unless
            # they are contained in existing_tree_df
            df = _process_properties(df, status, existing_tree_df=existing_tree_df)
            modified_items.update(df.modified_items)

            # Rectify paths
            df = _trim_unneeded_paths(df)
            df = _reify_missing_assets(df)

            # Pull children of items with IDs
            df = _pull_all_children_of_all_nodes(df, self._workbook_id, existing_tree_df,
                                                 item_ids_to_ignore=modified_items,
                                                 status=status)
            _increment_status_df(status, new_items=df)

            status_message = f"Tree successfully created from DataFrame."
            if existing_tree_df is not None:
                status_message += f' This tree modifies a pre-existing SPy-created tree with name ' \
                                  f'"{existing_tree_df.ID.iloc[0]}".'

        elif data and isinstance(data, str):
            if _common.is_guid(data):
                existing_node_id = data
            else:
                status.update(f'Searching for existing asset tree roots with name "{data}"', _common.Status.RUNNING)
                existing_node_id = _find_root_node_by_name(data, self._workbook_id, status)

            if existing_node_id:
                _initialize_status_df(status, 'Created', f'Pulling existing asset tree "{data}".',
                                      _common.Status.RUNNING)

                # Pull an existing tree. Detect whether it originated from SPy
                df = _pull_tree(existing_node_id, self._workbook_id, status=status)
                _increment_status_df(status, new_items=df)

                status_message = f"Recursively pulled {'SPy-created' if df.spy_tree else 'existing'} " \
                                 f"asset tree."
            else:
                _initialize_status_df(status, 'Created', f'Creating asset tree with new root "{data}".',
                                      _common.Status.RUNNING)

                # Define a brand new root asset
                df = pd.DataFrame([{
                    'Type': 'Asset',
                    'Path': '',
                    'Depth': 1,
                    'Name': data,
                    'Description': description if description else np.nan
                }], columns=_dataframe_columns)
                _increment_status_df(status, new_items=df)

                status_message = f'No existing root found. Tree created using new root "{data}".' \
                                 f'{"" if _login.client else " If an existing tree was expected, please log in."}'

        else:
            raise SPyTypeError("Input 'data' must be a name, name of a csv file, Seeq ID, or Metadata dataframe when "
                               "creating a Tree")

        _sort_by_node_path(df)
        if description:
            df.loc[0, 'Description'] = description
        if rename_root:
            df = _set_name(df, friendly_name)

        # Unlike in Tree.insert(), this final validation step will catch some user errors such as including two roots
        df = _validate_and_filter(df, status, errors, stage='final',
                                  error_message_header='Errors were encountered while creating tree',
                                  fatal_message='Errors were encountered while validating tree',
                                  subtract_errors_from_status=True)

        self._dataframe = df
        status.update(f'{status_message} {self.summarize(ret=True)}', _common.Status.SUCCESS)

    def insert(self, children=None, parent=None, *, friendly_name=None, formula=None, formula_parameters=None,
               errors=None, quiet=None, status=None):
        """
        Insert the specified elements into the tree.

        Parameters
        ----------
        children : {pandas.DataFrame, str, list, Tree}, optional
            Defines which element or elements will be inserted below each parent. If an existing
            node already existed at the level in the tree with that name (case-insensitive),
            it will be updated. If it doesn't already exist, a new node will be created
            (by deep-copy or reference if applicable).
            The following options are allowed:
            1) A basic string or list of strings to create a new asset.
            2) Another SPy Tree.
            3) spy.search results or other custom dataframes.

        parent : {pandas.DataFrame, str, int, list}, optional
            Defines which element or elements the children will be inserted below.
            If a parent match is not found and non-glob/regex string or path is used,
            the parent (or entire path) will be created too.
            The following options are allowed:
            1) No parent specified will insert directly to the root of the tree.
            2) String name match (case-insensitive equality, globbing, regex, column
                values) will find any existing nodes in the tree that match.
            3) String path match, including partial path matches.
            4) ID. This can either be the actual ID of the tree.push()ed node or the
                ID of the source item.
            5) Number specifying tree level. This will add the children below every
                node at the specified level in the tree (1 being the root node).
            6) spy.search results or other custom dataframe.

        friendly_name : str, optional
            Use this specified name rather than the referenced item's original name.

        formula : str, optional
            The formula for a calculated item. The `formula` and `formula_parameters` are
            used in place of the `children` argument.

        formula_parameters : dict, optional
            The parameters for a formula.

        errors : {'raise', 'catalog'}, optional
            If 'raise', any errors encountered will cause an exception. If 'catalog',
            errors will be added to a 'Result' column in the status.df DataFrame. This
            input will be used only for the duration of this function; it will default
            to the setting on the Tree if not specified.

        quiet : bool, optional
            If True, suppresses progress output. This input will be used only for the
            duration of this function; it will default to the setting on the Tree if
            not specified. Note that when status is provided, the quiet setting of
            the Status object that is passed in takes precedent.

        status : spy.Status, optional
            If specified, the supplied Status object will be updated as the command
            progresses. It gets filled in with the same information you would see
            in Jupyter in the blue/green/red table below your code while the
            command is executed. The table itself is accessible as a DataFrame via
            the status.df property.
        """

        _common.validate_argument_types([
            (children, 'children', (pd.DataFrame, Tree, str, list)),
            (parent, 'parent', (pd.DataFrame, list, str, int)),
            (friendly_name, 'friendly_name', str),
            (formula, 'formula', str),
            (formula_parameters, 'formula_parameters', (dict, list, str))
        ])
        errors = self._get_or_default_errors(errors)
        quiet = self._get_or_default_quiet(quiet)
        status = _common.Status.validate(status, quiet)

        if children is None:
            if not friendly_name:
                e = SPyValueError('Friendly Name must be specified if no children argument is given.')
                status.exception(e, throw=True)
            else:
                children = pd.DataFrame([{
                    'Name': friendly_name
                }])

        if isinstance(children, str):
            children = [children]
        if isinstance(children, list):
            for child in children:
                if not isinstance(child, str):
                    raise SPyValueError(f'List input to children argument contained non-string data: {child}')
            children = pd.DataFrame([{'ID': child} if _common.is_guid(child) else
                                     {'Name': child} for child in children])
        elif isinstance(children, Tree):
            children = children._dataframe.copy()

        if formula:
            if 'Formula' in children.columns or 'Formula Parameters' in children.columns:
                e = SPyValueError(
                    f"Children DataFrame cannot contain a 'Formula' or 'Formula Parameters' column when inserting a "
                    f"formula.")
                status.exception(e, throw=True)
            else:
                children['Formula'] = formula
                children['Formula Parameters'] = [formula_parameters] * len(children)

        _initialize_status_df(status, 'Inserted', 'Processing item properties and finding children to be inserted.',
                              _common.Status.RUNNING)

        # Check user input for errors, filter if errors='catalog'
        children = _validate_and_filter(children, status, errors, stage='input',
                                        error_message_header='Errors were encountered in input')

        children = children.reset_index(drop=True)

        if parent is not None and 'Parent' in children.columns:
            status.exception(SPyRuntimeError('If a "Parent" column is specified in the children dataframe, then the '
                                             'parent argument of the insert() method must be None'), throw=True)

        if _is_column_value_query(parent):
            children['Parent'] = children.apply(_fill_column_values, axis=1, query=parent)
        elif 'Parent' in children.columns:
            children['Parent'] = children.apply(_fill_column_values, axis=1, query_column='Parent')

        if friendly_name is not None:
            if _is_column_value_query(friendly_name):
                children['Friendly Name'] = friendly_name
            else:
                if len(children) > 1:
                    status.exception(SPyRuntimeError(
                        'friendly_name must be a column value query when multiple children are inputted'), throw=True)
                elif len(children) == 1:
                    children['Name'] = friendly_name
        _apply_friendly_name(children)

        # Sanitize data and pull in properties of items with IDs
        children = _process_properties(children, status, keep_parent_column=True)

        # Pull children of items with pre-existing IDs
        children = _pull_all_children_of_all_nodes(children, self._workbook_id, status=status)

        # Pre-insertion validation. This should only validate that we didn't pull in any metrics. We use
        # errors='catalog' so that the user isn't screwed when inserting an asset with threshold metric children
        children = _validate_and_filter(children, status, errors='catalog', stage='filter_out_metrics',
                                        error_message_header='Errors were encountered before inserting')

        def _get_children_to_add(children_df, parent_node):
            if 'Parent' in children_df.columns:
                children_to_add = children_df[children_df['Parent'].apply(_is_node_match, node=parent_node)].copy()
            else:
                children_to_add = children_df.copy()
            parent_full_path = _get_full_path(parent_node)
            if 'Path' in children_df.columns and not pd.isna(children_df['Path']).all():
                # Simplify path while maintaining subtree structure
                children_to_add = _trim_unneeded_paths(children_to_add, parent_full_path)
                children_to_add = _reify_missing_assets(children_to_add, parent_full_path)
            else:
                # No path found in the input children DF. All children will be below this parent.
                children_to_add['Path'] = parent_full_path
                children_to_add['Depth'] = parent_node['Depth'] + 1
            return children_to_add

        # If 'Parent' column is given, or parent argument has column values, define the parent matcher as this column
        if 'Parent' in children.columns:
            parent_pattern = children['Parent']
        else:
            parent_pattern = parent

        # We concatenate all children to be inserted into one dataframe before
        # inserting them using a single pd.merge call
        additions = [_get_children_to_add(children, row) for _, row in self._dataframe.iterrows()
                     if _is_node_match(parent_pattern, row)]
        additions = pd.concat(additions, ignore_index=True) if additions else pd.DataFrame()
        # Remove duplicate items in case the user has passed duplicate information to the children parameter
        _drop_duplicate_items(additions)

        _increment_status_df(status, new_items=additions)

        # Merge the dataframes on case-insensitive 'Path' and 'Name' columns
        working_df = _upsert(self._dataframe.copy(), additions)
        _sort_by_node_path(working_df)

        # If errors occur during the following validation step, they are "our fault", i.e., we inserted into the tree
        # incorrectly. We ideally want all feasible user errors to be reported before this point
        working_df = _validate_and_filter(working_df, status, errors, stage='final',
                                          error_message_header='Errors were encountered while inserting',
                                          fatal_message='Errors were encountered while validating tree',
                                          subtract_errors_from_status=True)
        self._dataframe = working_df

        if status.df.squeeze()['Total Items Inserted'] == 0 and status.df.squeeze()['Errors Encountered'] == 0:
            status.warn('No matching parents found. Nothing was inserted.')
        status.update(f'Successfully inserted items into the tree. {self.summarize(ret=True)}', _common.Status.SUCCESS)

    def remove(self, elements, *, errors=None, quiet=None, status=None):
        """
        Remove the specified elements from the tree recursively.

        Parameters
        ----------
        elements : {pandas.DataFrame, str, int}
            Defines which element or elements will be removed.
            1) String name match (case-insensitive equality, globbing, regex, column
                values) will find any existing nodes in the tree that match.
            2) String path match, including partial path matches.
            3) ID. This can either be the actual ID of the tree.push()ed node or the
                ID of the source item.
            4) Number specifying tree level. This will add the children below every
                node at the specified level in the tree (1 being the root node).
            5) spy.search results or other custom dataframe.

        errors : {'raise', 'catalog'}, optional
            If 'raise', any errors encountered will cause an exception. If 'catalog',
            errors will be added to a 'Result' column in the status.df DataFrame. This
            input will be used only for the duration of this function; it will default
            to the setting on the Tree if not specified.

        quiet : bool, optional
            If True, suppresses progress output. This input will be used only for the
            duration of this function; it will default to the setting on the Tree if
            not specified. Note that when status is provided, the quiet setting of
            the Status object that is passed in takes precedent.

        status : spy.Status, optional
            If specified, the supplied Status object will be updated as the command
            progresses. It gets filled in with the same information you would see
            in Jupyter in the blue/green/red table below your code while the
            command is executed. The table itself is accessible as a DataFrame via
            the status.df property.
        """

        _common.validate_argument_types([
            (elements, 'elements', (pd.DataFrame, str, int)),
            (errors, 'errors', str),
            (quiet, 'quiet', bool),
            (status, 'status', _common.Status)
        ])

        errors = self._get_or_default_errors(errors)
        quiet = self._get_or_default_quiet(quiet)
        status = _common.Status.validate(status, quiet)

        working_df = self._dataframe.copy()
        _initialize_status_df(status, 'Removed', 'Removing items from tree', _common.Status.RUNNING)

        idx = 1
        while idx < len(working_df.index):
            node = working_df.iloc[idx]
            if _is_node_match(elements, node):
                subtree_selector = working_df.index == idx
                subtree_selector = subtree_selector | (
                    working_df['Path'].str.casefold().str.startswith(_get_full_path(node).casefold(), na=False)
                )

                _increment_status_df(status, new_items=working_df[subtree_selector])
                working_df.drop(working_df.index[subtree_selector], inplace=True)
                working_df.reset_index(drop=True, inplace=True)
            else:
                idx += 1

        working_df = _validate_and_filter(working_df, status, errors, stage='final',
                                          error_message_header='Errors were encountered while removing',
                                          fatal_message='Errors were encountered while validating tree')
        self._dataframe = working_df

        if status.df.squeeze()['Total Items Removed'] == 0 and status.df.squeeze()['Errors Encountered'] == 0:
            status.warn('No matches found. Nothing was removed.')
        status.update(f'Successfully removed items from the tree. {self.summarize(ret=True)}',
                      _common.Status.SUCCESS)

    def move(self, source, destination=None, *, errors=None, quiet=None, status=None):
        """
        Move the specified elements (and all children) from one location in
        the tree to another.

        Parameters
        ----------
        source : {pandas.DataFrame, str}
            Defines which element or elements will be moved.
            1) String path match.
            2) ID. This can either be the actual ID of the tree.push()ed node or the
                ID of the source item.
            3) spy.search results or other custom dataframe.

        destination : {pandas.DataFrame, str}; optional
            Defines the new parent for the source elements.
            1) No destination specified will move the elements to just below
              the root of the tree.
            2) String path match.
            3) ID. This can either be the actual ID of the tree.push()ed node or the
                ID of the source item.
            4) spy.search results or other custom dataframe.

        errors : {'raise', 'catalog'}, optional
            If 'raise', any errors encountered will cause an exception. If 'catalog',
            errors will be added to a 'Result' column in the status.df DataFrame. This
            input will be used only for the duration of this function; it will default
            to the setting on the Tree if not specified.

        quiet : bool, optional
            If True, suppresses progress output. This input will be used only for the
            duration of this function; it will default to the setting on the Tree if
            not specified. Note that when status is provided, the quiet setting of
            the Status object that is passed in takes precedent.

        status : spy.Status, optional
            If specified, the supplied Status object will be updated as the command
            progresses. It gets filled in with the same information you would see
            in Jupyter in the blue/green/red table below your code while the
            command is executed. The table itself is accessible as a DataFrame via
            the status.df property.
        """

        _common.validate_argument_types([
            (source, 'source', (pd.DataFrame, str)),
            (destination, 'destination', (pd.DataFrame, str)),
            (errors, 'errors', str),
            (quiet, 'quiet', bool),
            (status, 'status', _common.Status)
        ])

        errors = self._get_or_default_errors(errors)
        quiet = self._get_or_default_quiet(quiet)
        status = _common.Status.validate(status, quiet)

        working_df = self._dataframe.copy()
        _initialize_status_df(status, 'Moved', 'Moving items in tree.', _common.Status.RUNNING)

        # Find the destination. Fail if there is not exactly one match for the input
        destination_node = working_df[working_df.apply(lambda node: _is_node_match(destination, node), axis=1)]
        if len(destination_node) == 0:
            status.exception(SPyValueError('Destination does not match any item in the tree.'), throw=True)
        elif len(destination_node) > 1:
            matched_names = '"%s"' % '", "'.join(destination_node.head(5).apply(_get_full_path, axis=1))
            status.exception(SPyValueError(f'Destination must match a single element of the tree. Specified '
                                           f'destination matches: "{matched_names}".'), throw=True)
        elif destination_node['Type'].iloc[0] != 'Asset':
            status.exception(SPyValueError('Destination must be an asset.'), throw=True)
        destination_path = _get_full_path(destination_node.iloc[0])

        # Find all source items, collect all of their children, and separate all matches into discrete subtrees.
        source_selector = working_df.apply(
            lambda node: _is_node_match(source, node) and node['Path'] != destination_path,
            axis=1
        )
        source_tree_roots = working_df[source_selector]
        for _, row in source_tree_roots.iterrows():
            source_selector = source_selector | working_df['Path'].str.startswith(_get_full_path(row), na=False)
        if source_selector[destination_node.index[0]]:
            status.exception(SPyValueError('Source cannot contain the destination'), throw=True)
        source_nodes = working_df[source_selector]

        def _split_selection_into_subtrees(df):
            if len(df) == 0:
                return []
            initial_depth = df.iloc[0]['Depth']

            above_initial_depth = df[df['Depth'] <= initial_depth]
            if len(above_initial_depth) == 1:
                return [df.copy()]
            next_subtree_index = above_initial_depth.index[1]

            first_subtree = df[df.index < next_subtree_index]
            others = df[df.index >= next_subtree_index]
            return [first_subtree.copy()] + _split_selection_into_subtrees(others)

        source_trees = _split_selection_into_subtrees(source_nodes)

        # Change path of each subtree, collect them into a single dataframe, and wipe any previously pushed IDs
        additions = [_trim_unneeded_paths(subtree, parent_full_path=destination_path) for subtree in source_trees]
        additions = pd.concat(additions, ignore_index=True) if additions else pd.DataFrame()
        additions['ID'] = np.nan

        _increment_status_df(status, new_items=additions)

        # Drop the old items and upsert the modified items
        working_df.drop(source_nodes.index, inplace=True)
        working_df = _upsert(working_df, additions)
        _sort_by_node_path(working_df)

        working_df = _validate_and_filter(working_df, status, errors, stage='final',
                                          error_message_header='Errors were encountered after moving',
                                          fatal_message='Errors were encountered after validation')
        self._dataframe = working_df

        if status.df.squeeze()['Total Items Moved'] == 0 and status.df.squeeze()['Errors Encountered'] == 0:
            status.warn('No matches found. Nothing was moved.')
        status.update(f'Successfully moved items within the tree. {self.summarize(ret=True)}',
                      _common.Status.SUCCESS)

    @property
    def size(self):
        """
        Property that gives the number of elements currently in the tree.
        """
        return len(self._dataframe)

    def __len__(self):
        return self.size

    @property
    def height(self):
        """
        Property that gives the current height of the tree. This is the length
        of the longest item path within the tree.
        """
        return self._dataframe['Depth'].max()

    def items(self):
        return self._dataframe.copy()

    def count(self, item_type=None):
        """
        Count the number of elements in the tree of each Seeq type. If item_type
        is not specified, then returns a dictionary with keys 'Asset', 'Signal',
        'Condition', 'Scalar', and 'Unknown'. If item_type is specified, then
        returns an int.

        Parameters
        ----------
        item_type : {'Asset', 'Signal', 'Condition', 'Scalar', 'Uncompiled Formula'}, optional
            If specified, then the method will return an int representing the
            number of elements with Type item_type. Otherwise, a dict will be
            returned.
        """

        simple_types = ['Asset', 'Signal', 'Condition', 'Scalar', 'Uncompiled Formula']
        if item_type:
            if not isinstance(item_type, str) or item_type.capitalize() not in (simple_types + ['Formula',
                                                                                                'Uncompiled']):
                raise SPyValueError(f'"{item_type}" is not a valid node type. Valid types are: '
                                    f'{", ".join(simple_types)}')
            if item_type in ['Uncompiled Formula', 'Uncompiled', 'Formula']:
                return sum(pd.isnull(self._dataframe['Type']) | (self._dataframe['Type'] == ''))
            else:
                return sum(self._dataframe['Type'].str.contains(item_type.capitalize(), na=False))

        def _simplify_type(t):
            if not pd.isnull(t):
                for simple_type in simple_types:
                    if simple_type in t:
                        return simple_type
            return 'Uncompiled Formula'

        return self._dataframe['Type'] \
            .apply(_simplify_type) \
            .value_counts() \
            .to_dict()

    def summarize(self, ret=False):
        """
        Generate a human-readable summary of the tree.

        Parameters
        ----------
        ret : bool, default False
            If True, then this method returns a string summary of the tree. If
            False, then this method prints the summary and returns nothing.
        """
        counts = self.count()

        def _get_descriptor(k, v):
            singular_descriptors = {
                key: key.lower() if key != 'Uncompiled Formula' else 'calculation whose type has not '
                                                                     'yet been determined'
                for key in counts.keys()
            }
            plural_descriptors = {
                key: f'{key.lower()}s' if key != 'Uncompiled Formula' else 'calculations whose types have not '
                                                                           'yet been determined'
                for key in counts.keys()
            }
            if v == 1:
                return singular_descriptors[k]
            else:
                return plural_descriptors[k]

        nonzero_counts = {k: v for k, v in counts.items() if v != 0}
        if len(nonzero_counts) == 1:
            count_string = ''.join([f'{v} {_get_descriptor(k, v)}' for k, v in nonzero_counts.items()])
        elif len(nonzero_counts) == 2:
            count_string = ' and '.join([f'{v} {_get_descriptor(k, v)}' for k, v in nonzero_counts.items()])
        elif len(nonzero_counts) > 2:
            count_string = ', '.join([f'{v} {_get_descriptor(k, v)}' for k, v in nonzero_counts.items()])
            last_comma = count_string.rfind(',')
            count_string = count_string[:last_comma + 2] + 'and ' + count_string[last_comma + 2:]
        else:
            return

        root_name = self._dataframe.iloc[0]['Name']

        summary = f'The tree "{root_name}" has height {self.height} and contains {count_string}.'

        if ret:
            return summary
        else:
            print(summary)

    def missing_items(self, return_type='print'):
        """
        Identify elements that may be missing child elements based on the contents of other sibling nodes.

        Parameters
        ----------
        return_type : {'print', 'string', 'dict'}, default 'print'
            If 'print', then a string that enumerates the missing items will be
            printed. If 'string', then that same string will be returned and not
            printed. If 'dict', then a dictionary that maps element paths to lists
            of their potential missing children will be returned.
        """
        if return_type.lower() not in ['print', 'str', 'string', 'dict', 'dictionary', 'map']:
            raise SPyValueError(f"Illegal argument {return_type} for return_type. Acceptable values are 'print', "
                                f"'string', and 'dict'.")
        return_type = return_type.lower()

        if self.count(item_type='Asset') == self.size:
            missing_string = 'There are no non-asset items in your tree.'
            if return_type in ['dict', 'dictionary', 'map']:
                return dict()
            elif return_type == 'print':
                print(missing_string)
                return
            else:
                return missing_string

        repeated_grandchildren = dict()

        prev_row = None
        path_stack = []
        for _, row in self._dataframe.iterrows():
            if prev_row is None:
                pass
            elif row.Depth > prev_row.Depth:
                path_stack.append((prev_row, set()))
            else:
                path_stack = path_stack[:row.Depth - 1]
            if len(path_stack) > 1:
                grandparent, grandchildren_set = path_stack[-2]
                if row.Name in grandchildren_set:
                    repeated_grandchildren.setdefault(_get_full_path(grandparent), set()).add(row.Name)
                else:
                    grandchildren_set.add(row.Name)
            prev_row = row

        missing_item_map = dict()
        path_stack = []
        for _, row in self._dataframe.iterrows():
            if prev_row is None:
                pass
            elif row.Depth > prev_row.Depth:
                if path_stack and _get_full_path(path_stack[-1][0]) in repeated_grandchildren:
                    required_children = repeated_grandchildren[_get_full_path(path_stack[-1][0])].copy()
                else:
                    required_children = set()
                path_stack.append((prev_row, required_children))
            else:
                for parent, required_children in path_stack[row.Depth - 1:]:
                    if len(required_children) != 0:
                        missing_item_map[_get_full_path(parent)] = sorted(required_children)
                path_stack = path_stack[:row.Depth - 1]
            if len(path_stack) != 0:
                _, required_children = path_stack[-1]
                required_children.discard(row.Name)
            prev_row = row
        for parent, required_children in path_stack:
            if len(required_children) != 0:
                missing_item_map[_get_full_path(parent)] = sorted(required_children)

        if return_type in ['dict', 'dictionary', 'map']:
            return missing_item_map

        if len(missing_item_map):
            missing_string = 'The following elements appear to be missing:'
            for parent_path, missing_children in missing_item_map.items():
                missing_string += f"\n{parent_path} is missing: {', '.join(missing_children)}"
        else:
            missing_string = 'No items are detected as missing.'

        if return_type == 'print':
            print(missing_string)
        else:
            return missing_string

    @property
    def name(self):
        return self._dataframe.loc[0, 'Name']

    @name.setter
    def name(self, value):
        _common.validate_argument_types([(value, 'name', str)])

        df = _set_name(self._dataframe, value)
        _validate_and_filter(df, _common.Status(quiet=True), errors='raise', stage='final',
                             error_message_header='Errors encountered after changing tree root name')

        self._dataframe = df

    def push(self, *, errors=None, quiet=None, status=None):
        """
        Imports the tree into Seeq Server.

        errors : {'raise', 'catalog'}, optional
            If 'raise', any errors encountered will cause an exception. If 'catalog',
            errors will be added to a 'Result' column in the status.df DataFrame. This
            input will be used only for the duration of this function; it will default
            to the setting on the Tree if not specified.

        quiet : bool, optional
            If True, suppresses progress output. This input will be used only for the
            duration of this function; it will default to the setting on the Tree if
            not specified. Note that when status is provided, the quiet setting of
            the Status object that is passed in takes precedent.

        status : spy.Status, optional
            If specified, the supplied Status object will be updated as the command
            progresses. It gets filled in with the same information you would see
            in Jupyter in the blue/green/red table below your code while the
            command is executed. The table itself is accessible as a DataFrame via
            the status.df property.
        """
        errors = self._get_or_default_errors(errors)
        quiet = self._get_or_default_quiet(quiet)
        status = _common.Status.validate(status, quiet)

        df_to_push = _format_formula_parameters(self._dataframe, status)

        push_results = _push.push(metadata=df_to_push, workbook=self._workbook, archive=True,
                                  errors=errors, quiet=quiet, status=status)

        # make root only asset tree appear in Data -> Asset Trees in workbench
        if self.height == 1:
            trees_api = TreesApi(_login.client)
            item_id_list = ItemIdListInputV1()
            item_id_list.items = list(push_results.ID)
            trees_api.move_nodes_to_root_of_tree(body=item_id_list)

        successfully_pushed = push_results['Push Result'] == 'Success'
        self._dataframe.loc[successfully_pushed, 'ID'] = push_results.loc[successfully_pushed, 'ID']
        self._dataframe.loc[successfully_pushed, 'Type'] = push_results.loc[successfully_pushed, 'Type']

        return push_results

    def _ipython_display_(self):
        self.summarize()

    def __iter__(self):
        return self._dataframe.itertuples(index=False, name='Item')

    def _find_workbook_id(self, quiet, status):
        """
        Set the _workbook_id based on the workbook input. This will enable us to know whether we should set
        the `ID` or `Referenced ID` column when pulling an item.
        """
        if _common.is_guid(self._workbook):
            self._workbook_id = _common.sanitize_guid(self._workbook)
        elif _login.client:
            search_query, _ = _push.create_analysis_search_query(self._workbook)
            search_df = spy.workbooks.search(search_query,
                                             quiet=quiet,
                                             status=status.create_inner('Find Workbook', quiet=quiet))
            self._workbook_id = search_df.iloc[0]['ID'] if len(search_df) > 0 else _common.EMPTY_GUID
        else:
            self._workbook_id = _common.EMPTY_GUID

    def _get_or_default_errors(self, errors_input):
        if isinstance(errors_input, str):
            _common.validate_errors_arg(errors_input)
            return errors_input
        return self.errors

    def _get_or_default_quiet(self, quiet_input):
        if isinstance(quiet_input, bool):
            return quiet_input
        return self.quiet


def _get_full_path(node):
    if not isinstance(_common.get(node, 'Name'), str) or len(node['Name']) == 0:
        return ''
    if isinstance(_common.get(node, 'Path'), str) and len(node['Path']) != 0:
        return f"{node['Path']} >> {node['Name']}"
    return node['Name']


def _sort_by_node_path(df):
    _decorate_with_full_path(df)
    df.sort_values(by='Full Path List', inplace=True, ignore_index=True)
    _remove_full_path(df)


def _decorate_with_full_path(df):
    """
    From the 'Path' and 'Name' columns, add a 'Full Path List' column.
    """
    df.loc[:, 'Full Path List'] = df.apply(_get_full_path, axis=1).apply(_common.path_string_to_list)


def _remove_full_path(df):
    """
    Remove the 'Full Path List' column.
    """
    df.drop('Full Path List', axis=1, inplace=True)


def _update_path_from_full_path_list(df):
    """
    From the 'Full Path List' column, set the 'Path' column.
    """
    df['Path'] = df.apply(lambda node: _common.path_list_to_string(node['Full Path List'][:-1]), axis=1)


def _set_name(df, new_name):
    df = df.copy()
    old_name = df.loc[0, 'Name']

    df.loc[0, 'Name'] = new_name
    pattern = re.compile(r'^' + re.escape(old_name) + r'(?=\s*>>|$)', flags=re.IGNORECASE)
    df['Path'] = df['Path'].str.replace(pattern, new_name)
    df['ID'] = np.nan

    return df


def _trim_unneeded_paths(df, parent_full_path=None, maintain_last_shared_root=None):
    """
    Remove any leading parts of the path that are shared across all rows. Then add the parent_path back onto the
    front of the path.

    E.G. If all rows have a path of 'USA >> Texas >> Houston >> Cooling Tower >> Area {x} >> ...',
    'Cooling Tower' would become the root asset for this Tree. Then if parent_path was 'My Tree >> Cooling Tower',
    all rows would have a path 'My Tree >> Cooling Tower >> Area {x} >> ...'
    """
    if len(df) == 0:
        return df

    # Get the path of the first node. It doesn't matter which we start with since we're only removing paths that are
    # shared across ALL rows.
    _decorate_with_full_path(df)
    shared_root = _push.get_common_root(df['Full Path List'])
    # Trim the path until we're left with the last universally shared node.
    while shared_root:
        trimmed_full_path_list = df['Full Path List'].apply(lambda l: l[1:])
        remaining_shared_root = _push.get_common_root(trimmed_full_path_list)
        keep_last_shared_root = True
        if parent_full_path and remaining_shared_root:
            # We only want to remove the root-most path if it is already going to be the parent (due to insert)
            parent_name = _common.path_string_to_list(parent_full_path)[-1]
            keep_last_shared_root = remaining_shared_root != parent_name
        elif parent_full_path and shared_root and isinstance(maintain_last_shared_root, bool):
            # We explicitly want to remove the last shared root so it can be replaced.
            keep_last_shared_root = maintain_last_shared_root
        if not remaining_shared_root and keep_last_shared_root:
            # We need to keep the last shared root so do not save trimmed_full_path_list
            break
        df['Full Path List'] = trimmed_full_path_list
        if 'Depth' in df:
            df['Depth'] -= 1
        shared_root = remaining_shared_root

    if parent_full_path:
        # Prepend the parent path if applicable
        parent_path_list = _common.path_string_to_list(parent_full_path)
        parent_name = parent_path_list[-1]
        if _push.get_common_root(df['Full Path List']) == parent_name:
            parent_path_list.pop()
        if parent_path_list:
            df['Full Path List'] = df['Full Path List'].apply(lambda l: parent_path_list + l)
            if 'Depth' in df:
                df['Depth'] += len(parent_path_list)
    _update_path_from_full_path_list(df)
    _remove_full_path(df)
    return df


def _get_shared_root(full_path_series):
    """
    Returns the highest shared name in the input paths. If no such name exists, returns None
    """
    first_full_path_list = full_path_series.iloc[0]
    if not len(first_full_path_list):
        return None
    root_name = first_full_path_list[0]
    all_roots_same = full_path_series.apply(lambda l: len(l) and l[0] == root_name).all()
    return root_name if all_roots_same else None


def _reify_missing_assets(df, existing_parent_path=None):
    """
    Automatically generate any assets that are referred to by path only.
    E.G. If this tree were defined using a dataframe containing only leaf signals, but with a Path column of
    'Cooling Tower >> Area {x} >> {signal}', the 'Cooling Tower' and 'Area {x}' assets would be generated.

    If existing_parent_path is provided, the reification will not occur for any existing parents.
    E.G. 'Example >> Cooling Tower >> Area {x} >> {signal}' with existing_parent_path='Example'
     would only generate 'Cooling Tower' and 'Area {x}' assets, not 'Example'.
    """
    # Store the Full Path tuples of all possible Assets to be created in a set
    full_paths = set()
    for path_list in df.apply(_get_full_path, axis=1).apply(_common.path_string_to_list):
        full_paths.update([tuple(path_list[:i]) for i in range(1, len(path_list))])
    # Remove all Assets whose paths are contained in the existing_parent_path
    if existing_parent_path is not None:
        full_paths.difference_update([full_path for full_path in full_paths if
                                      _common.path_list_to_string(full_path) in existing_parent_path])
    # Create dataframe rows based on these paths, and use a single pd.merge call to update the dataframe
    new_assets = pd.DataFrame([{
        'Type': 'Asset',
        'Path': _common.path_list_to_string(full_path[:-1]),
        'Name': full_path[-1],
        'Depth': len(full_path)
    } for full_path in full_paths])
    _drop_duplicate_items(new_assets)
    return _upsert(df, new_assets, prefer_right=False)


def _pull_tree(node_id, workbook_id, status=None):
    """
    Given the ID of an Item, pulls that node and all children and returns the resulting sanitized dataframe
    """
    # Determine if node_id is root of pre-existing SPy tree
    existing_tree_df = _get_existing_spy_tree(pd.DataFrame([{'ID': node_id}]), workbook_id=workbook_id)

    # Get the requested node itself
    df = _process_properties(pd.DataFrame([{'ID': node_id}], columns=_dataframe_columns),
                             status=status,
                             existing_tree_df=existing_tree_df)

    df = _pull_all_children_of_all_nodes(df, workbook_id, existing_tree_df, status=status)
    _common.add_properties_to_df(df, spy_tree=existing_tree_df is not None)

    return df


def _pull_all_children_of_all_nodes(df, workbook_id, existing_tree_df=None, item_ids_to_ignore=None, status=None):
    """
    For each node in the tree that contains an 'ID' or 'Referenced ID', pull in any asset tree children.
    If any nodes already exist in the dataframe (by case-insensitive Path+Name), the existing row will be kept.
    """
    if df.empty:
        return df

    for col in ['ID', 'Referenced ID']:
        if col not in df.columns:
            df[col] = pd.Series(np.nan, dtype='object')
    # Gather all Paths+IDs into a list upfront
    items_to_pull_children = df[(~pd.isnull(df['ID'])) | (~pd.isnull(df['Referenced ID']))]

    for _, row in items_to_pull_children.iterrows():
        # Pull based on ID if it exists, otherwise use Referenced ID
        if _common.present(row, 'ID'):
            node_id = row['ID']
            row_is_reference = False
        else:
            node_id = row['Referenced ID']
            row_is_reference = True
        node_full_path = _get_full_path(row)
        parent_value = _common.get(row, 'Parent')
        df = _pull_all_children_of_node(df, node_id, node_full_path, workbook_id,
                                        existing_tree_df=existing_tree_df if not row_is_reference else None,
                                        item_ids_to_ignore=item_ids_to_ignore,
                                        parent_value=parent_value,
                                        status=status)
    return df


def _pull_all_children_of_node(df, node_id, node_full_path, workbook_id, existing_tree_df, item_ids_to_ignore,
                               parent_value, status):
    """
    Given the ID of an Item in an asset tree, pulls all children and places them into the given dataframe.
    Does not overwrite existing data.
    """
    # Get all children of the requested asset
    search_results = _search.search(query={'Asset': node_id}, all_properties=True, workbook=workbook_id,
                                    order_by=['ID'], quiet=True)
    if len(search_results) == 0:
        return df

    if item_ids_to_ignore is not None:
        search_results = search_results[~search_results['ID'].isin(item_ids_to_ignore)]
        if len(search_results) == 0:
            return df

    _increment_status_df(status, pulled_items=search_results)

    # Step 1: Convert the search results dataframe into a Tree-style dataframe.
    insert_df = _process_properties(search_results, status, existing_tree_df=existing_tree_df, pull_nodes=False)
    # If we are pulling additional children to be inserted into the Tree, and a 'Parent' column is specified,
    #  we must propagate it to pulled children
    if parent_value is not None:
        insert_df['Parent'] = parent_value

    # Step 2: If the node_id's original name does not match what the node's name is in the Tree, trim off any extra
    # path from the input.
    _decorate_with_full_path(insert_df)
    parent_name = _common.path_string_to_list(node_full_path)[-1]
    if parent_name:
        maintain_last_shared_root = parent_name in insert_df.iloc[0]['Full Path List']
        insert_df = _trim_unneeded_paths(insert_df, node_full_path, maintain_last_shared_root)

    # Step 3: Actually insert the nodes
    df = _upsert(df, insert_df, prefer_right=False)
    return df


def _upsert(df1, df2, prefer_right=True):
    """
    Upserts the data from df2 into df1 based on case-insensitive Path and Name values.
    If a row from df2 matches a row in df1, and the two have conflicting values, then preference
    is given as per the prefer_right parameter. Keeps the columns of df1
    """
    if len(df2) == 0:
        return df1
    if len(df1) == 0:
        return df2

    orig_columns = df1.columns
    df1 = df1.copy()
    df2 = df2.copy()
    for df in (df1, df2):
        df['path_nocase'] = df.Path.astype('object').str.casefold()
        df['name_nocase'] = df.Name.astype('object').str.casefold()
    df = df1.merge(df2, how='outer', on=['path_nocase', 'name_nocase'])
    wipe_ids = pd.Series(False, index=df.index)
    for column in orig_columns:
        prefer_right_column = prefer_right and column not in ['Path', 'Name']
        left_column = column + '_x'
        right_column = column + '_y'
        if right_column in df.columns:
            prefer_column = right_column if prefer_right_column else left_column
            backup_column = left_column if prefer_right_column else right_column
            df[column] = df[prefer_column]
            missing_values = pd.isnull(df[column])
            df.loc[missing_values, column] = df.loc[missing_values, backup_column]
            df[column] = df[column].apply(_safe_int_cast)
            if column == 'Type' and 'ID' in df.columns:
                wipe_ids = wipe_ids | df.apply(lambda row: _type_differs(row[prefer_column], row[backup_column]),
                                               axis=1)
    df.drop(columns=df.columns.difference(orig_columns), inplace=True)
    if 'ID' in df.columns:
        df.loc[wipe_ids, 'ID'] = np.nan
    return df


def _type_differs(t1, t2):
    if pd.isnull(t1) or pd.isnull(t2) or len(t1) == 0 or len(t2) == 0:
        return False
    if 'Calculated' in t1 and 'Stored' in t2:
        return False
    if 'Stored' in t1 and 'Calculated' in t2:
        return False
    for simple_type in ('Asset', 'Scalar', 'Signal', 'Condition'):
        if simple_type in t1 and simple_type in t2:
            return False
    return True


def _drop_duplicate_items(df):
    """
    Removes duplicate items (identified by case-insensitive Path and Name) from a dataframe.
    """
    if len(df) == 0:
        return
    df['path_nocase'] = df.Path.astype('object').str.casefold()
    df['name_nocase'] = df.Name.astype('object').str.casefold()
    df.drop_duplicates(subset=['path_nocase', 'name_nocase'], inplace=True, ignore_index=True)
    df.drop(columns=['path_nocase', 'name_nocase'], inplace=True)


def _safe_int_cast(x):
    return int(x) if isinstance(x, float) and not np.isnan(x) and x == int(x) else x


def _is_column_value_query(s):
    if not isinstance(s, str):
        return False
    if re.search(r'\{\{.*\}.*\}', s):
        return True
    return False


def _fill_column_values(row, query: str = None, query_column=None):
    """
    Fills a column values query with actual column values from a row in a dataframe. Returns the output string
    """
    if pd.isnull(query):
        if query_column not in row:
            return np.nan
        query = row[query_column]
        if pd.isnull(query):
            return np.nan

    def _fill_column_value(col_val_query_match: re.Match):
        col_val_query = col_val_query_match[1]
        col, extract_pattern = re.fullmatch(r'\{(.*?)\}(.*)', col_val_query).groups(default='')
        if not _common.present(row, col):
            raise SPyValueError('Not a match')
        value = str(row[col])
        if extract_pattern == '':
            return value

        # Match against a glob pattern first, then try regex
        for pattern in (_glob_with_capture_groups_to_regex(extract_pattern), extract_pattern):
            try:
                extraction = re.fullmatch(pattern, value)
                if extraction:
                    if len(extraction.groups()) != 0:
                        return extraction[1]
                    else:
                        return extraction[0]
            except re.error:
                # There may be a compilation error if the input wasn't intended to be interpreted as regex
                continue
        raise SPyValueError('Not a match')

    try:
        return re.sub(r'\{(\{.*?\}.*?)\}', _fill_column_value, query)
    except SPyValueError:
        return np.nan


def _glob_with_capture_groups_to_regex(glob):
    """
    Converts a glob to a regex, but does not escape parentheses, so that the glob can be written with capture groups
    """
    return re.sub(r'\\(\(|\))', r'\1', fnmatch.translate(glob))


def _is_node_match(pattern, node):
    """
    General pattern matcher for tree methods that match on tree items. Input options for pattern:

    None
        Matches the root

    np.nan
        Matches nothing. This is used when the user inserts via a 'Parent' column in the children
        dataframe that is only specified for some children.

    int
        Matches all items of the specified depth.

    GUID
        Matches items that have ID or Referenced ID equal to pattern

    Path/Name match
        If just a name is given, matching will be attempted when interpreting the string as
        1) a case-insensitive exact query
        2) a globbing pattern
        3) a regex pattern
        If path markers '>>' are included, the pieces of the path will be split and matched like above
        to find items whose paths end with the path query given.

    list
        Iterates over all elements and calls this same function. If any match is found, return True

    pd.Series
        Checks if this is a DataFrame row containing 'ID' or 'Name' in its index. If so, tries to match
        on ID and then Path/Name. If not, then treated like an iterable in the same way as a list

    pd.DataFrame
        Checks if any of the rows are a match
    """
    if pattern is None:
        return node['Depth'] == 1
    if pd.api.types.is_scalar(pattern) and pd.isnull(pattern):
        # This case handles when the user only gives the 'Parent' column for some children, or gives a parent
        #  string that uses column values that aren't valid for some rows.
        return False
    if isinstance(pattern, pd.DataFrame):
        return pattern.apply(_is_node_match, axis=1, node=node).any()
    if isinstance(pattern, list):
        if len(pattern) == 0:
            return False
        else:
            # Pass on to next isinstance() check
            pattern = pd.Series(pattern)
    if isinstance(pattern, pd.Series):
        # First interpret the Series as a dataframe row being matched up against the tree dataframe row
        if _common.present(pattern, 'ID'):
            return pattern['ID'] == _common.get(node, 'ID') or pattern['ID'] == _common.get(node, 'Referenced ID')
        if _common.present(pattern, 'Name'):
            if _common.present(pattern, 'Path') and _determine_path(pattern).casefold() != node['Path'].casefold():
                return False
            return pattern['Name'].casefold() == node['Name'].casefold()
        if len(pattern.index.intersection(node.index)) != 0:
            return False

        # Now interpret the Series as a collection of patterns to check against
        return pattern.apply(_is_node_match, node=node).any()
    if isinstance(pattern, str):
        if _common.is_guid(pattern):
            if isinstance(node['ID'], str) and pattern.upper() == node['ID'].upper():
                return True
            if isinstance(node['Referenced ID'], str) and pattern.upper() == node['Referenced ID'].upper():
                return True
        else:
            regex_list = _node_match_string_to_regex_list(pattern)
            return _is_node_match_via_regex_list(regex_list, node)
    if isinstance(pattern, int):
        return node['Depth'] == pattern
    return False


def _node_match_string_to_regex_list(pattern):
    """
    :param pattern: String name match (case-insensitive equality, globbing, regex, column values)
                    or string path match (full or partial; case-insensitive equality, globbing, or regex)
    :return: A list of regular expressions that match the last n names in the full path of a node.
    """
    patterns = _common.path_string_to_list(pattern)
    return [_exact_or_glob_or_regex(p) for p in patterns]


def _exact_or_glob_or_regex(pat):
    try:
        re.compile(pat)
        return re.compile('(?i)' + '(' + ')|('.join([re.escape(pat), fnmatch.translate(pat), pat]) + ')')
    except re.error:
        return re.compile('(?i)' + '(' + ')|('.join([re.escape(pat), fnmatch.translate(pat)]) + ')')


def _is_node_match_via_regex_list(pattern_list, node):
    path_list = _common.path_string_to_list(_get_full_path(node))
    offset = len(path_list) - len(pattern_list)
    if offset < 0:
        return False
    for i in range(len(pattern_list)):
        if not pattern_list[i].fullmatch(path_list[offset + i]):
            return False
    return True


def _find_root_nodes(workbook_id, matcher):
    trees_api = TreesApi(_login.client)
    matching_root_nodes = list()

    offset = 0
    limit = _config.options.search_page_size
    kwargs = dict()
    # Can't use get_tree_root_nodes()'s `properties` filter for scoped_to because the endpoint is case-sensitive and
    # we want both global and scoped nodes.
    if workbook_id and workbook_id is not _common.EMPTY_GUID:
        kwargs['scoped_to'] = workbook_id

    keep_going = True
    while keep_going:
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        root_nodes = trees_api.get_tree_root_nodes(**kwargs)  # type: AssetTreeOutputV1
        for root_node in root_nodes.children:  # type: TreeItemOutputV1
            if matcher(root_node):
                # A root node matching the name was already found. Choose a best_root_node based on this priority:
                # Workbook-scoped SPy assets > workbook-scoped assets > global SPy assets > global assets
                workbook_scoped_score = 2 if root_node.scoped_to is not None else 0
                spy_created_score = 1 if _item_output_has_sdl_datasource(root_node) else 0
                setattr(root_node, 'score', workbook_scoped_score + spy_created_score)
                matching_root_nodes.append(root_node)
        keep_going = root_nodes.next is not None
        offset = offset + limit
    return matching_root_nodes


def _find_root_node_by_name(name, workbook_id, status):
    """
    Finds the Seeq ID of a case-insensitive name match of existing root nodes.
    """
    if not _login.client:
        # User is not logged in or this is a unit test. We must create a new tree.
        return None
    status.update('Finding best root.', _common.Status.RUNNING)

    name_pattern = re.compile('(?i)^' + re.escape(name) + '$')
    matching_root_nodes = _find_root_nodes(workbook_id, lambda root_node: name_pattern.match(root_node.name))
    if len(matching_root_nodes) == 0:
        status.update(f"No existing root items were found matching '{name}'.", _common.Status.RUNNING)
        return None
    best_score = max([getattr(n, 'score') for n in matching_root_nodes])
    best_root_nodes = list(filter(lambda n: getattr(n, 'score') == best_score, matching_root_nodes))
    if len(best_root_nodes) > 1:
        e = SPyValueError(
            f"More than one existing tree was found with name '{name}'. Please use an ID to prevent ambiguities.")
        status.exception(e, throw=True)
    best_id = best_root_nodes[0].id
    if len(matching_root_nodes) > 1:
        status.update(f"{len(matching_root_nodes)} root items were found matching '{name}'. Selecting {best_id}.",
                      _common.Status.RUNNING)
    return best_id


def _apply_friendly_name(df):
    if 'Friendly Name' not in df.columns or df['Friendly Name'].isnull().all():
        _common.add_properties_to_df(df, modified_items=set())
        return

    # If we are changing the names of items in a dataframe whose paths are dependent on one another, then
    # record those dependencies so we can modify paths afterwards as well
    path_relationships = _path_relationships(df)

    modified_items = set()
    for i in df.index:
        if pd.isnull(df.loc[i, 'Friendly Name']):
            continue
        if _is_column_value_query(df.loc[i, 'Friendly Name']):
            new_name = _fill_column_values(df.loc[i], df.loc[i, 'Friendly Name'])
        else:
            new_name = df.loc[i, 'Friendly Name']
        if pd.isnull(new_name):
            continue
        df.loc[i, 'Name'] = new_name
        if _common.present(df.loc[i], 'ID'):
            modified_items.add(df.loc[i, 'ID'])

    _recover_relationships(df, path_relationships)
    _common.add_properties_to_df(df, modified_items=modified_items)


def _path_relationships(df):
    """
    Return a dict of dicts indicating via integers how the paths of the input rows are dependent on one another.

    Example:
        df = pd.DataFrame([{
            'Path': 'Root', 'Name': 'Item 1'
        }, {
            'Path': 'Root >> Item 1', 'Name': 'Item 2'
        }])

        output = {
            1: { # 1 refers here to the row in df with index 1, i.e., Item 2
                1: 0 # 1 refers here to the item in Item 2's path with index 1, i.e. 'Item 1'
                     # 0 refers here to the index of Item 1's row in df
            }
        }
    """
    if len(df) == 0 or 'Name' not in df.columns:
        return None
    temp_df = df[['Name']].copy()
    temp_df['Path'] = df.apply(_determine_path, axis=1)
    full_paths = list(temp_df.apply(_get_full_path, axis=1).apply(_common.path_string_to_list))
    relationships = dict()
    # This is O(n^2) but it's not a core feature
    for i, this in enumerate(full_paths):
        if this == [''] or len(this) == 0:
            continue
        for j, other in enumerate(full_paths):
            if other == ['']:
                continue
            # If the full path "other" begins with the full path "this", then we mark that
            # the (len(this) - 1)th element in "other"'s path is equal to "this"
            if len(other) > len(this) and other[:len(this)] == this:
                if j not in relationships:
                    relationships[j] = dict()
                relationships[j][len(this) - 1] = i
    return relationships


def _recover_relationships(df, relationships):
    """
    Takes a list of relationships (in the format described in _path_relationships) and modifies paths in
    df to reflect those relationships
    """
    if relationships is None:
        return
    for i, path_ref_dict in relationships.items():
        path = _determine_path(df.loc[i])
        path_list = _common.path_string_to_list(path) if path else []
        for j, reference in path_ref_dict.items():
            if 0 <= reference < len(df) and 0 <= j < len(path_list):
                path_list[j] = df.loc[reference, 'Name']
        df.loc[i, 'Path'] = _common.path_list_to_string(path_list)
    if 'Asset' in df.columns:
        df.drop(columns='Asset', inplace=True)


def _process_properties(df, status, existing_tree_df=None, pull_nodes=True, keep_parent_column=False):
    """
    Sanitize and pull item properties into an input dataframe. Steps in order:
    -- Pulls missing properties for items with ID provided
    -- Filters out properties not in _dataframe_columns
    -- Determines tree depth
    -- Determines (if possible_tree_copy is True) if the input dataframe corresponds to an existing SPy tree
        -- If it is indeed a copy of a SPy tree, pulls in calculations from the original tree
        -- Otherwise, it converts all items with IDs into references
    -- Ensures all formula parameters are NAN or dict
    """
    df = df.reset_index(drop=True)

    df = df.apply(_process_row_properties, axis=1,
                  status=status,
                  pull_nodes=pull_nodes,
                  keep_parent_column=keep_parent_column)

    def _row_is_from_existing_tree(row):
        if existing_tree_df is None or not _common.present(row, 'ID'):
            return 'new'
        same_id_rows = existing_tree_df[existing_tree_df.ID.str.casefold() == row['ID'].casefold()]
        if len(same_id_rows) != 1:
            return 'new'
        if _common.present(row, 'Type') and row['Type'].casefold() != same_id_rows.Type.iloc[0].casefold():
            return 'new'
        if _common.present(row, 'Name') and row['Name'].casefold() != same_id_rows.Name.iloc[0].casefold():
            return 'modified'
        if _common.present(row, 'Path') and row['Path'].casefold() != same_id_rows.Path.iloc[0].casefold():
            return 'modified'
        return 'pre-existing'

    row_type = df.apply(_row_is_from_existing_tree, axis=1)
    modified_items = df.loc[row_type == 'modified', 'ID'] if 'ID' in df.columns else set()

    # For the nodes that originated from the pre-existing SPy tree we are modifying, we want to pull
    # pre-existing calculations directly.
    formulas_api = FormulasApi(_login.client)
    df.loc[row_type == 'pre-existing', :] = df.loc[row_type == 'pre-existing', :].apply(_pull_calculation, axis=1,
                                                                                        formulas_api=formulas_api)

    # For the nodes that originate from places other than the pre-existing SPy tree we are modifying,
    # we want to build references so we create and modify *copies* and not the original items.
    df.loc[row_type != 'pre-existing', :] = df.loc[row_type != 'pre-existing', :].apply(_make_node_reference, axis=1)

    if 'Formula Parameters' in df.columns:
        df['Formula Parameters'] = df['Formula Parameters'].apply(_formula_parameters_to_dict)

    _common.add_properties_to_df(df, modified_items=modified_items)

    return df


def _process_row_properties(row, status, pull_nodes, keep_parent_column):
    if _common.present(row, 'ID') and pull_nodes:
        new_row = _pull_node(row['ID'])
        _increment_status_df(status, pulled_items=[new_row])
    else:
        new_row = pd.Series(index=_dataframe_columns, dtype='object')

    # In case that properties are specified, but IDs are given, the user-given properties
    # override those pulled from Seeq
    for prop, value in row.items():
        if prop in ['Path', 'Asset']:
            prop = 'Path'
            value = _determine_path(row)
        elif prop == 'Type' and _common.present(new_row, 'Type') and _type_differs(value, new_row['Type']):
            new_row['ID'] = np.nan
        _add_tree_property(new_row, prop, value)

    if not _common.present(new_row, 'Type') and not _common.present(new_row, 'Formula'):
        new_row['Type'] = 'Asset'

    if not _common.present(new_row, 'Path'):
        new_row['Path'] = ''
    new_row['Depth'] = new_row['Path'].count('>>') + 2 if new_row['Path'] else 1

    if keep_parent_column and _common.present(row, 'Parent'):
        new_row['Parent'] = row['Parent']

    return new_row


def _make_node_reference(row):
    row = row.copy()
    if _common.present(row, 'ID'):
        if _common.get(row, 'Type') in _data_types and not is_reference(row):
            _metadata.build_reference(row)
        if _common.present(row, 'ID'):
            row['Referenced ID'] = row['ID']
    row['ID'] = np.nan
    return row


def is_reference(row):
    if not _common.get(row, 'Referenced ID') or not _common.get(row, 'Formula Parameters'):
        return False
    formula = _common.get(row, 'Formula')
    if formula is not None and re.match(r'^\$\w+$', formula):
        return True
    else:
        return False


def _pull_calculation(row, formulas_api):
    if _common.get(row, 'Type') in _calculated_types and _common.present(row, 'ID'):
        row = row.copy()
        formula_output = formulas_api.get_item(id=row['ID'])  # type: FormulaItemOutputV1
        row['Formula'] = formula_output.formula
        row['Formula Parameters'] = [
            '%s=%s' % (p.name, p.item.id if p.item else p.formula) for p in formula_output.parameters
        ]
    return row


def _pull_node(node_id):
    """
    Returns a dataframe row corresponding to the item given by node_id
    """
    items_api = _login.get_api(ItemsApi)

    item_output = items_api.get_item_and_all_properties(id=node_id)  # type: ItemOutputV1
    node = pd.Series(index=_dataframe_columns, dtype='object')

    # Extract only the properties we use
    node['Name'] = item_output.name
    node['Type'] = item_output.type
    node['ID'] = item_output.id  # If this should be a copy, it'll be converted to 'Referenced ID' later
    for prop in item_output.properties:  # type: PropertyOutputV1
        _add_tree_property(node, prop.name, prop.value)

    return node


def _add_tree_property(properties, key, value):
    """
    If the property is one which is used by SPy Trees, adds the key+value pair to the dict.
    """
    if key in _dataframe_columns:
        value = _common.none_to_nan(value)
        if isinstance(value, str) and key in ['Cache Enabled', 'Archived', 'Enabled', 'Unsearchable']:
            # Ensure that these are booleans. Otherwise Seeq Server will silently ignore them.
            value = (value.lower() == 'true')
        if key not in properties or not (pd.api.types.is_scalar(value) and pd.isnull(value)):
            properties[key] = value
    return properties


def _item_output_has_sdl_datasource(item_output):
    for prop in item_output.properties:  # type: PropertyOutputV1
        if prop.name == 'Datasource Class' and prop.value == _common.DEFAULT_DATASOURCE_CLASS:
            return True
    return False


def _get_existing_spy_tree(df, workbook_id):
    if 'ID' not in df.columns or not _login.client:
        return None

    df = df[df['ID'].notnull()]
    if 'Path' in df.columns:
        df = df[(df['Path'] == '') | (df['Path'].isnull())]

    def _spy_tree_root_filter(root):
        return root.scoped_to is not None and _item_output_has_sdl_datasource(root)

    existing_spy_trees = _find_root_nodes(workbook_id, _spy_tree_root_filter)

    def _row_is_spy_tree_root(_row, root_id, root_name):
        try:
            assert _common.present(_row, 'ID') and _row['ID'].casefold() == root_id.casefold()
            assert not _common.present(_row, 'Name') or _row['Name'].casefold() == root_name.casefold()
            assert not _common.get(_row, 'Path')
            return True
        except AssertionError:
            return False

    df_root_id = None
    for spy_tree in existing_spy_trees:
        for _, row in df.iterrows():
            if _row_is_spy_tree_root(row, spy_tree.id, spy_tree.name):
                if df_root_id is None:
                    df_root_id = row['ID']
                else:
                    return None
    if df_root_id is not None:
        existing_tree_df = spy.search([{'ID': df_root_id}, {'Asset': df_root_id}], workbook=workbook_id,
                                      order_by=['ID'], quiet=True)
        existing_tree_df['Path'] = existing_tree_df.apply(_determine_path, axis=1)
        existing_tree_df = existing_tree_df[['ID', 'Path', 'Name', 'Type']]
        return existing_tree_df
    else:
        return None


def _determine_path(row):
    """
    Gets the path from the Path and Asset columns
    """
    path = _common.get(row, 'Path')
    asset = _common.get(row, 'Asset')
    if not isinstance(path, str):
        path = None
    if not isinstance(asset, str):
        asset = None
    return ' >> '.join([s for s in (path, asset) if s is not None])


def _formula_parameters_to_dict(formula_parameters):
    if isinstance(formula_parameters, dict) or (pd.api.types.is_scalar(formula_parameters) and pd.isnull(
            formula_parameters)):
        return formula_parameters

    if isinstance(formula_parameters, str):  # formula_parameters == 'x=2b17adfd-3308-4c03-bdfb-bf4419bf7b3a'
        # handle an empty string case
        if len(formula_parameters) == 0:
            return dict()
        else:
            formula_parameters = [formula_parameters]

    if isinstance(formula_parameters, pd.Series):
        formula_parameters = formula_parameters.tolist()

    formula_dictionary = dict()
    if isinstance(formula_parameters, list):  # formula_parameters == ['x=2b17adfd-3308-4c03-bdfb-bf4419bf7b3a', ...]
        for param in formula_parameters:  # type: str
            split_list = param.split('=')  # ['x', '2b17...']
            if len(split_list) != 2:
                raise SPyException(f'Formula Parameter: {param} needs to be in the format \'paramName=inputItem\'.')
            formula_dictionary[split_list[0].strip()] = split_list[1].strip()
    return formula_dictionary  # output == {'x': '2b17adfd-3308-4c03-bdfb-bf4419bf7b3a'}


def _format_formula_parameters(df, status):
    output_df = df.copy()

    output_formula_parameters_column = pd.Series(np.nan, index=output_df.index, dtype='object')

    # Takes relative-path formula parameters and changes them to full path for the ensuing push call
    for idx, row in output_df[output_df['Formula Parameters'].notnull()].iterrows():
        formula_parameters = copy.deepcopy(row['Formula Parameters'])

        for name, item in row['Formula Parameters'].items():
            if not isinstance(item, str) or _common.is_guid(item):
                continue
            item_full_path = _get_full_path({'Path': row['Path'], 'Name': item})

            resolved_path = None
            for _, other_row in output_df.iterrows():
                if other_row is row:
                    continue
                if _is_node_match(item_full_path, other_row):
                    resolved_path = _get_full_path(other_row)
            if resolved_path is None:
                # Validation prevents this error from being raised
                e = SPyValueError(f"Issue resolving formula parameters for item at '{row.Path} >> "
                                  f"{row.Name}'. No matches were found for '{item_full_path}'.")
                status.exception(e, throw=True)
            formula_parameters[name] = resolved_path

        output_formula_parameters_column[idx] = formula_parameters

    output_df['Formula Parameters'] = output_formula_parameters_column
    return output_df


def _initialize_status_df(status, action, *args):
    status.df = pd.DataFrame([{
        f'Assets {action}': 0,
        f'Signals {action}': 0,
        f'Conditions {action}': 0,
        f'Scalars {action}': 0,
        f'Total Items {action}': 0,
        f'Items Pulled From Seeq': 0,
        f'Errors Encountered': 0
    }], index=['Status'])
    status.update(*args)


def _increment_status_df(status, new_items=None, pulled_items=None, error_items=None, subtract_errors=False):
    if new_items is not None:
        for column in status.df.columns:
            if 'Type' in new_items.columns:
                for item_type in ['Asset', 'Signal', 'Condition', 'Scalar']:
                    if item_type in column:
                        status.df[column] += sum(new_items['Type'].fillna('').str.contains(item_type))
            if 'Total' in column:
                status.df[column] += len(new_items)
    if pulled_items is not None:
        status.df['Items Pulled From Seeq'] += len(pulled_items)
    if error_items is not None:
        if subtract_errors:
            for column in status.df.columns:
                if 'Type' in error_items.columns:
                    for item_type in ['Asset', 'Signal', 'Condition', 'Scalar']:
                        if item_type in column:
                            status.df[column] -= sum(error_items['Type'].fillna('').str.contains(item_type))
                if 'Total' in column:
                    status.df[column] -= len(error_items)
        status.df['Errors Encountered'] += len(error_items)
    status.update()


def _process_csv_data(data, status, workbook=_common.DEFAULT_WORKBOOK_PATH):
    """
    Processes a csv file into an appropriate dataframe for Tree constructor
    :param data: str
            Filename of a CSV
    :param status: spy.Status
            The status object to pass warnings to
    :param workbook: str, default 'Data Lab >> Data Lab Analysis'
            The path to a workbook (in the form of 'Folder >> Path >> Workbook Name')
            or an ID that all pushed items will be 'scoped to'. You can
            push to the Corporate folder by using the following pattern:
            '__Corporate__ >> Folder >> Path >> Workbook Name'. A Tree currently
            may not be globally scoped. These items will not be visible/searchable
            using the data panel in other workbooks.
    :return: pandas.Dataframe
    """

    status.update('Reading CSV data', _common.Status.RUNNING)

    try:
        csv_data = pd.read_csv(data)
    except FileNotFoundError:
        message = (f"File {data} not found. Please ensure you have it in the correct working "
                   f"directory.")
        status.exception(SPyValueError(message), throw=True)
    except BaseException as e:
        message = f"Unexpected {e}, {type(e)}"
        status.exception(SPyValueError(message), throw=True)

    csv_columns = list(csv_data.columns)
    levels = [i for i in csv_columns if 'Level' in i]

    # validation
    if 'Name' not in csv_columns and 'ID' not in csv_columns:
        message = f"A 'Name' or 'ID' column is required"
        status.exception(SPyValueError(message), throw=True)

    join_column = _get_complete_column_for_join(csv_data, csv_columns, status)

    if _is_first_row_of_levels_columns_blank(csv_data, levels):
        message = f"All Level columns must have a value in the first row"
        status.exception(SPyValueError(message), throw=True)

    # forward fill Levels columns
    csv_data.loc[:, levels] = csv_data.loc[:, levels].ffill()

    if join_column == 'Name':
        csv_data = _get_ids_by_name_from_user_input(csv_data, status, workbook=workbook)

    return csv_data


def _is_first_row_of_levels_columns_blank(csv_data, levels) -> bool:
    return csv_data[levels].iloc[0].isnull().any()


def _get_complete_column_for_join(csv_data, csv_columns, status):
    name_id = csv_data[[x for x in ['Name', 'ID'] if x in csv_columns]]
    join_cols = list(name_id.columns[~name_id.isnull().any()])
    if len(join_cols) == 0:
        message = f"Either 'Name' or 'ID' column must be complete, without missing values."
        status.exception(SPyValueError(message), throw=True)
    elif len(join_cols) == 2:
        join_col = 'ID'
    else:
        join_col = join_cols[0]
    return join_col


def _make_paths_from_levels(csv_data):
    """
    Gets the path from a series of levels columns, adds that to the
    dataframe, and removes the levels columns
    :param csv_data: pandas.Dataframe
    :return: None
    """

    def make_path(row, levels):
        path = " >> ".join([row[i] for i in levels if not _is_nan_or_string_nan(row[i])])
        return path

    level_cols = [i for i in list(csv_data.columns) if 'Level' in i]
    if len(level_cols) == 0 and 'Path' in list(csv_data.columns):
        return

    elif len(level_cols) == 0:
        # there's no levels columns and no path
        raise SPyValueError(f"Levels columns or a path column must be provided")

    else:
        csv_data['Path'] = csv_data.apply(make_path, axis=1, levels=level_cols)
        csv_data.drop(columns=level_cols, inplace=True)


def _is_nan_or_string_nan(item):
    if not pd.isnull(item):
        if isinstance(item, str):
            return item.lower() == "nan"
        return False
    return True


def _get_ids_by_name_from_user_input(input_df, status, workbook=_common.DEFAULT_WORKBOOK_PATH):
    """
    Adds IDs from search to a dataframe, searches based on 'Name'
    :param input_df: pandas.Dataframe
    :param status: spy.Status
    :param workbook: str, default 'Data Lab >> Data Lab Analysis'
            The path to a workbook (in the form of 'Folder >> Path >> Workbook Name')
            or an ID that all pushed items will be 'scoped to'. You can
            push to the Corporate folder by using the following pattern:
            '__Corporate__ >> Folder >> Path >> Workbook Name'. A Tree currently
            may not be globally scoped. These items will not be visible/searchable
            using the data panel in other workbooks.
    :return: pandas.Dataframe
    """

    status.update('Searching for items from CSV', _common.Status.RUNNING)

    _search_options = ['Name', 'Type']

    if 'ID' in input_df.columns:
        # rows with IDs, no search needed
        df_with_ids = input_df.dropna(subset=['ID'])

        # rows without IDs, to search by name
        df_no_ids = input_df[input_df['ID'].isnull()].copy()

    else:
        df_with_ids = pd.DataFrame()
        df_no_ids = input_df

    if 'ID' in df_no_ids.columns:
        df_no_ids.drop(columns=['ID'], inplace=True)

    # which of the options the csv has:
    search_cols = [x for x in _search_options if x in df_no_ids.columns]

    try:
        search_res = spy.search(df_no_ids[search_cols], order_by=["ID"], workbook=workbook, quiet=True)[['Name', 'ID']]
    except KeyError:
        status.warn(f"The following names did not return search results and were "
                    f"ignored: {list(df_no_ids['Name'])}")
        return df_with_ids

    # add warning for Names with multiple search results
    multiples = search_res.loc[search_res.duplicated(subset=['Name']), 'Name']
    if len(multiples) > 0:
        status.warn(f"The following names returned multiple search results, "
                    f"so the first result was used: {list(set(multiples))}")
        search_res = search_res.drop_duplicates(subset=['Name'], keep='first').reset_index(drop=True)

    # inner merge the search results with data from csv
    name_data = df_no_ids.merge(search_res, left_on='Name', right_on='Name')

    # add warning for Names without search results
    expected_names = set()
    found_names = set()
    found_names.update(name_data['Name'])
    expected_names.update(df_no_ids['Name'])
    missing_names = expected_names.difference(found_names)
    if len(missing_names) > 0:
        status.warn(f"The following names did not return search results and were "
                    f"ignored: {list(missing_names)}")

    all_data = pd.concat([name_data, df_with_ids], axis=0, ignore_index=True)

    return all_data


def _validate_and_filter(df_to_validate, status, errors, stage, error_message_header, fatal_message=None,
                         raise_if_all_filtered=False, subtract_errors_from_status=False):
    """
    This is the main validation function. It takes a dataframe as input, and returns a dataframe containing the rows
    for which no errors were found, and a dataframe containing the rows for which errors were found.

    :param df_to_validate: DataFrame input
    :param status: Status object to raise exception to if error is found and errors='raise'
    :param errors: Determines whether errors raise an exception or are catalogued in the output

    :param stage: {'input', 'filter_out_metrics', 'final'} This must be a key in _property_validations. Indicates which
    property validations we want to perform on df_to_validate, depending on whether it is a user-input
    dataframe, a dataframe about to be saved to Tree._dataframe, or some intermediary dataframe. Additionally,
    we only check the tree structure of the dataframe if stage='final'

    :param error_message_header: The error message header to pass to the exception if one is raised
    :param fatal_message: When stage='final' and errors='catalog', we always double check that validation is
    successful on a filtered dataframe. If not, then we raise an exception with fatal_message as the header

    :return filtered_df: A validated dataframe with invalid rows removed
    """
    raise_if_all_filtered = raise_if_all_filtered or stage == 'final'
    error_summaries, error_series = _validate(df_to_validate, stage)
    if len(error_summaries) != 0:
        if errors == 'raise':
            df_to_validate['Error Message'] = error_series
            status.df = df_to_validate[error_series != '']
            _raise_error_summaries(error_message_header, error_summaries, status)
        else:
            keep_items = error_series == ''
            bad_results = df_to_validate[~keep_items].copy()
            bad_results['Error Message'] = error_series[~keep_items]
            filtered_df = df_to_validate[keep_items].reset_index(drop=True)
            _increment_status_df(status, error_items=bad_results, subtract_errors=subtract_errors_from_status)

            if raise_if_all_filtered and filtered_df.empty:
                status.df = bad_results
                status.warn('All rows encountered errors and tree could not be constructed')
                _raise_error_summaries(error_message_header, error_summaries, status)

            if stage == 'final':
                # We validate again to ensure that self._dataframe will stay valid. Something is fatally wrong
                # with validation if the following code is reached.
                further_error_summaries, error_series = _validate(filtered_df)
                if len(further_error_summaries) != 0:
                    filtered_df['Error Message'] = error_series
                    status.df = filtered_df[error_series != '']
                    _raise_error_summaries(fatal_message if fatal_message else 'Tree validation failed',
                                           error_summaries, status)

            _warn_error_summaries(error_message_header, error_summaries, status)

            return _rectify_column_order(filtered_df)
    else:
        return _rectify_column_order(df_to_validate)


def _validate(df, stage='final'):
    error_summaries_properties, error_series_properties = _validate_properties(df, stage)
    if stage == 'final':
        # Only do tree validation in the final validation step, i.e., when this df represents a tree
        # Don't do tree validation on rows that had property errors
        ignore_rows = error_series_properties != ''
        error_summaries_tree, error_series_tree = _validate_tree_structure(df, ignore_rows=ignore_rows)
    else:
        error_summaries_tree, error_series_tree = [], pd.Series('', index=df.index)

    error_summaries = error_summaries_properties + error_summaries_tree
    error_series = _update_error_msg(error_series_properties, error_series_tree)

    return error_summaries, error_series


def _get_error_message(header_message, error_summaries):
    msg = header_message
    if len(error_summaries) == 1:
        msg += ': ' + error_summaries[0]
    else:
        msg += ':\n- ' + '\n- '.join(error_summaries[:MAX_ERRORS_DISPLAYED])
    if len(error_summaries) > MAX_ERRORS_DISPLAYED:
        additional_errors = len(error_summaries) - MAX_ERRORS_DISPLAYED
        msg += f'\n- {additional_errors} additional issue{"s" if additional_errors > 1 else ""} found.'
    return msg


def _raise_error_summaries(header_message, error_summaries, status):
    msg = _get_error_message(header_message, error_summaries)
    status.exception(SPyRuntimeError(msg), throw=True)


def _warn_error_summaries(header_message, error_summaries, status):
    msg = _get_error_message(header_message, error_summaries)
    status.warn(msg)
    status.update()


def _update_error_msg(old_msg, new_msg):
    if new_msg is None or isinstance(new_msg, str) and new_msg == '':
        return old_msg
    out = old_msg + ' ' + new_msg
    if isinstance(out, pd.Series):
        return out.str.strip()
    else:
        return out.strip()


def _validate_tree_structure(df, ignore_rows=None):
    # Asserts that:
    # - The tree is non-empty
    # - The root doesn't have a path, and is the only item with depth 1
    # - The dataframe is sorted by path
    # - There are no missing assets referenced in paths
    # - Paths reflect names of preceding items
    # - Depths reflects lengths of paths

    size = len(df)
    if size == 0:
        return ['Tree must be non-empty.'], pd.Series(dtype='string')

    error_series = pd.Series('', index=df.index)
    error_summaries = []
    if ignore_rows is None:
        ignore_rows = pd.Series(False, index=df.index)

    prev_path = list()
    prev_type = 'Asset'
    _decorate_with_full_path(df)
    for i, row in df.iterrows():
        if error_series.iloc[i]:
            # Node has an error message already due to a bad ancestor
            continue

        depth = row.Depth
        this_path = row['Full Path List']

        try:
            if ignore_rows[i]:
                # Ignore tree errors on this row because of a property validation error
                # We still want invalidate its children if possible, so we raise an assertion error with no message
                assert False, ''

            assert depth == len(this_path), 'Item\'s depth does not match its path.'

            if i == 0:
                assert len(this_path) == 1, 'The root of the tree cannot be assigned a path.'
                # The following assertion will be handled differently to include node names in the error message
                assert (df['Full Path List'].iloc[1:].apply(len) != 1).all(), 'A tree can only have one root but ' \
                                                                              'multiple were given: '
            else:
                assert depth >= 1, 'Only depths greater or equal to 1 are valid.'

            if depth <= len(prev_path):
                assert prev_path[:depth - 1] == this_path[:depth - 1], 'Item\'s position in tree ' \
                                                                       'does not match its path.'
                assert prev_path[depth - 1] != this_path[depth - 1], 'Item has the same name and path ' \
                                                                     'of another item in the tree.'
                assert prev_path[depth - 1] < this_path[depth - 1], 'Item is not stored in proper ' \
                                                                    'position sorted by path.'
            else:
                assert depth == len(prev_path) + 1, 'Item has an ancestor not stored in this tree.'
                assert prev_path[:depth - 1] == this_path[:depth - 1], 'Item\'s position in tree ' \
                                                                       'does not match its path.'
                assert prev_type == 'Asset', 'Item\'s parent must be an Asset.'

            prev_path = this_path
            prev_type = row.Type

        except AssertionError as e:
            message = str(e)
            if message.startswith('A tree can only have one root'):
                roots = df.Depth == 1
                message += '"%s".' % '\", \"'.join(df.Name[roots])
                error_series[roots] = message
                error_series[~roots] = 'Item\'s parent is invalid.'
                error_summaries.append(message)
                break
            error_series[i] = message
            children = df['Full Path List'].apply(
                lambda path: len(path) > len(this_path) and path[:len(this_path)] == this_path)
            error_series[children] = 'Item\'s parent is invalid.'
            if message:
                error_summaries.append(f'Invalid item with path "{" >> ".join(this_path)}": ' + message)

    _remove_full_path(df)

    return error_summaries, error_series


def _validate_properties(df, stage):
    """
    :param df: The dataframe to be validated for errors related to presence of properties, type of properties,
    and ill-defined properties
    """
    error_series = pd.Series('', index=df.index)
    error_message_map = dict()  # maps error messages to the rows that encountered the error
    for index, node in df.iterrows():
        errors = _validate_node_properties(node, stage, df)
        for error in errors:
            _common.get(error_message_map, error, default=list(), assign_default=True).append((index, node))
        if errors:
            error_series[index] = ' '.join(errors)

    error_summaries = _collect_error_messages(error_message_map)

    # TODO CRAB-24296 Validate calculations better
    return error_summaries, error_series


def _collect_error_messages(error_message_map):
    def _get_row_description(index, row):
        description_properties = dict()
        # Prefer Friendly Name over Name
        if _common.present(row, 'Friendly Name'):
            description_properties['friendly name'] = row['Friendly Name']
        elif _common.present(row, 'Name'):
            description_properties['name'] = row['Name']
        # If a Name or Friendly Name has been found, add a Path too if it is present
        if len(description_properties) != 0 and (_common.present(row, 'Path') or _common.present(row, 'Asset')):
            description_properties['path'] = _determine_path(row)
        # Use ID next if it is present
        if len(description_properties) == 0 and _common.present(row, 'ID'):
            description_properties['ID'] = row['ID']

        # Use index if none of the above are present
        if len(description_properties) == 0:
            return f'item with index {index}'
        else:
            return 'item with ' + ' and '.join([f'{prop_name} "{prop_value}"' for prop_name, prop_value in
                                                description_properties.items()])

    def _get_row_descriptiveness_score(row):
        _, row = row
        if _common.present(row, 'Name') or _common.present(row, 'Friendly Name'):
            if _common.present(row, 'Path') or _common.present(row, 'Asset'):
                return 3
            else:
                return 2
        elif _common.present(row, 'ID'):
            return 1
        else:
            return 0

    def _get_most_descriptive_row(_rows):
        index, row = max(_rows, key=_get_row_descriptiveness_score)
        return _get_row_description(index, row)

    collected_messages = list()
    for message, rows in error_message_map.items():
        if len(collected_messages) >= MAX_ERRORS_DISPLAYED:
            # No need to fuss with error messaging formatting that won't be displayed. We pass in placeholder string
            collected_messages.extend(('' for _ in range(len(error_message_map) - MAX_ERRORS_DISPLAYED)))
            break
        if len(rows) == 1:
            collected_messages.append(f'Issue with {_get_row_description(*rows[0])}: {message}')
        else:
            collected_messages.append(f'Issue with {_get_most_descriptive_row(rows)} and '
                                      f'{len(rows) - 1} other row{"s" if len(rows) > 2 else ""}: {message}')
    return collected_messages


def _validate_node_properties(node, stage, df):
    def has_bad_type(column, dtype):
        if _common.present(node, column):
            datum = _safe_int_cast(node[column])
            try:
                _common.validate_argument_types([(datum, '', dtype)])
            except TypeError:
                return True
        return False

    def dtype_names(dtype):
        if isinstance(dtype, tuple):
            return tuple(x.__name__ for x in dtype)
        return dtype.__name__

    errors = [f"The property '{column}' must have one of the following types: {dtype_names(dtype)}."
              for column, dtype in _dataframe_dtypes.items() if has_bad_type(column, dtype)]

    # The conditions in _property_validations assume that values have the correct datatype
    # Therefore, return only type errors if they exist.
    if errors:
        return errors
    errors += [message for requirement, message in _property_validations(node, stage) if not requirement]

    # Similarly return property validations before validating formula parameters
    if errors:
        return errors
    if stage == 'final':
        errors += _get_dependency_errors(node, df)
    return errors


def _get_dependency_errors(node, df):
    if not _common.present(node, 'Formula Parameters') or not isinstance(node['Formula Parameters'], dict):
        return list()

    errors = list()
    for param in node['Formula Parameters'].values():
        if not isinstance(param, str) or _common.is_guid(param):
            continue
        param_full_path = _get_full_path({'Path': node['Path'], 'Name': param})
        matches = df[df.apply(lambda row: _is_node_match(param_full_path, row), axis=1)]
        if len(matches) == 0:
            errors.append(f'Formula parameter is invalid, missing, or has been removed from tree: "{param_full_path}".')
        elif len(matches) > 1:
            matched_names = '"%s"' % '", "'.join([_get_full_path(row) for _, row in matches.iterrows()])
            errors.append(f'Formula parameter "{param_full_path}" matches multiple items in tree: {matched_names}.')
        elif _common.get(matches.iloc[0], 'Type') == 'Asset':
            errors.append(f'Formula parameter "{param_full_path}" is an asset. Formula parameters must be conditions, '
                          f'scalars, or signals.')
    return errors


def _no_repeated_nested_paths(path_list, name, recurse=True):
    if len(path_list) == 0:
        return True
    if path_list[-1] == name:
        return False
    return _no_repeated_nested_paths(path_list[:-1], path_list[-1]) if recurse else True


def _rectify_column_order(df):
    standard_columns = [col for col in _dataframe_columns if col in df.columns]
    extra_columns = sorted([col for col in df.columns if col not in _dataframe_columns])
    columns = standard_columns + extra_columns
    return df[columns]


def _property_validations(node, stage):
    if stage == 'input':
        return [
            (_common.get(node, 'ID') or _common.get(node, 'Name') or _common.get(node, 'Friendly Name'),
             "The property 'Name' or 'Friendly Name' is required for all nodes without ID."),
            (not _common.get(node, 'Type') or _common.get(node, 'Formula') or
             ('Condition' not in node['Type'] and 'Signal' not in node['Type']) or
             _common.get(node, 'ID'),
             "Stored Signals and Conditions are not yet supported. "
             "All Signals and Conditions require either a formula or an ID."),
            (not _common.present(node, 'Formula Parameters') or _common.present(node, 'Formula'),
             "Must have a Formula if Formula Parameters are defined."),
            # TODO CRAB-24637 check required properties for metrics and remove the below
            (not _common.present(node, 'Type') or 'Metric' not in _common.get(node, 'Type'),
             "Threshold Metrics are not yet supported."),
            (not (_common.present(node, 'ID') or _common.present(node, 'Referenced ID')) or _login.client,
             "Must log in via spy.login() before inserting an item via ID or Referenced ID."),
            (not _common.present(node, 'ID') or _common.is_guid(node['ID']),
             f"The property 'ID' must be a valid GUID. Given: '{_common.get(node, 'ID')}'"),
            (not _common.present(node, 'Referenced ID') or _common.is_guid(node['Referenced ID']),
             f"The property 'Referenced ID' must be a valid GUID. Given: '{_common.get(node, 'Referenced ID')}'"),
            (not (_common.get(node, 'Path') and _common.get(node, 'Name')) or
             _no_repeated_nested_paths(_common.path_string_to_list(node['Path']), node['Name']),
             "Paths with repeated names are not valid."),
            ((not (_common.present(node, 'Formula') or _common.present(node, 'Formula Parameters'))
              or not _common.get(node, 'Type') == 'Asset'),
             "Assets cannot have formulas or formula parameters.")
        ]
    elif stage == 'filter_out_metrics':
        return [
            # TODO CRAB-24637 check required properties for metrics and remove the below
            (not _common.present(node, 'Type') or 'Metric' not in _common.get(node, 'Type'),
             "Threshold Metrics are not yet supported.")
        ]
    elif stage == 'final':
        return [
            (_common.get(node, 'Formula') or _common.get(node, 'Type'),
             "The property 'Type' is required for all items without formulas."),
            (not _common.get(node, 'Type') or _common.get(node, 'Formula') or
             ('Condition' not in node['Type'] and 'Signal' not in node['Type']),
             "Stored Signals and Conditions are not yet supported. All Signals and Conditions require a formula."),
            (not _common.present(node, 'Formula Parameters') or _common.present(node, 'Formula'),
             "Must have a Formula if Formula Parameters are defined."),
            # TODO CRAB-24637 check required properties for metrics and remove the below
            (not _common.present(node, 'Type') or 'Metric' not in _common.get(node, 'Type'),
             "Threshold Metrics are not yet supported."),
            (_common.present(node, 'Name'),
             "The property 'Name' is required."),
            (_common.present(node, 'Path'),
             "The property 'Path' is required."),
            (_common.present(node, 'Depth'),
             "The property 'Depth' is required."),
            (not _common.present(node, 'Name') or not _common.present(node, 'Path') or
             _no_repeated_nested_paths(_common.path_string_to_list(node['Path']), node['Name'],
                                       recurse=False),
             f"Paths with repeated names are not valid."),
            ((not (_common.present(node, 'Formula') or _common.present(node, 'Formula Parameters'))
              or not _common.get(node, 'Type') == 'Asset'),
             "Assets cannot have formulas or formula parameters."),
        ]
