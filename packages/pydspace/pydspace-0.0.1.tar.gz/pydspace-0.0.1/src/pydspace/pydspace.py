import matlab
import matlab.engine
import numpy as np

def dspace(*args, path: str = None) -> matlab.engine:
    """
    This function its just a python rewrite of the dspace.m function provided
    in the dSpace matlab package. You can find more documentation in that
    respective file.

    Args:
        args: Either numpy arrays, or (name,value) pairs.
        path: Path of the directory where dspace is located.
    Returns:
        Matlab engine object.
    """
    input_names = []
    input_values = []

    num_args = len(args)
    i = 0
    while i < num_args:
        # Check if the arguments follow a (name, value) scheme and
        # proceed correspondingly.
        if isinstance(args[i], str):
            if i == num_args - 1 :
                error_msg = (
                    f"dspace: The last function input {i} is a string {args[i]}.\n"
                    "Strings can only occur in name, value pairs"
                    "(to give names to labels or features).\nInput ignored."

                )
                print(error_msg)
                break
                # raise ValueError(error_msg)

            name, value = args[i], args[i+1]

            # If the next argument is also an string, ignore those
            # two elements.
            if isinstance(value, str):
                error_msg = (
                    f"dspace: Function inputs {i} and {i+1} are both strings"
                    f" {name}, {value}.\n"
                    "Strings can only occur in name, value pairs"
                    "(to give names to labels or features).\nInput ignored."
                )
                i = i + 2
                print(error_msg)
                continue

            # Check if next argument is indeed a numpy array.
            # TODO: We must be able to use different dataypes not only
            # numpy arrays
            if not isinstance(value, np.ndarray):
                error_msg = (
                    f"dspace: Function input {i} is a string {name}.\n"
                    f"The next input must be a numpy.ndarray but is not.\n"
                    "Input ignored."
                )
                i = i + 2
                print(error_msg)
                continue

            # Create input from the name, value pair.
            # TODO: Make sure the name can be used in Matlab code.
            input_names.append(name)
            input_values.append(value)

            i = i + 2

        else:
            # TODO: In Matlab it is possible to get name of the variable
            # passed as argument to a function with 'inputname'. In Python
            # there is not a clean way to do this, therefore for the moment
            # if no names are passed, each value will get as name 'input_i'.
            name = f"name_{i}" 
            value = args[i]

            input_names.append(name)
            input_values.append(value)

            i = i + 1
    

    assert len(input_names) == len(input_values)

    # Transform the np.ndarray to matlab matrices
    for i in range(len(input_values)):
        matrix = input_values[i]
        input_values[i] = matlab.double(matrix.tolist())

        # Free the memory inmediatly
        del matrix


    # Start the Matlab Engine
    engine = matlab.engine.start_matlab()
    engine.addpath(path, nargout=0)

    # In the ideal case we would like to operate on the object
    # returned by the parseDspaceArgs matlab function, but the matlab api
    # for python does not allow it, so instead we just call the function and 
    # save the output in the workspace, then we use eval. An issue is that,
    # then the variable is a global one and not a local one, so naming bugs
    # could appear.
    # TODO: There might be a cleaner way to do this.

    engine.workspace["source_pydspace"] = engine.dspace.parseDspaceArgs(
        input_values,
        input_names,
        1,
        nargout = 1
    )

    instr_1 = "source_pydspace.createdBy = 'Import through dspace() function.';"
    instr_2 = "source_pydspace.createdOn = now();"

    engine.eval(instr_1, nargout=0)
    engine.eval(instr_2, nargout=0)

    source = engine.workspace["source_pydspace"]
    engine.dspace(source, nargout=0)

    # We must return the engine. Since we created it as a local 
    # variable if we don't return it, then it will just get deleted from the 
    # stack (i.e the engine gets killed the , and dspace will not open.

    # TODO: Maybe it's useful to also return the dspaceApp, dSource and the
    # dView

    return engine

def add_feature(engine: matlab.engine, name: str) -> None:
    """
    Just a test function to see the capibilities of the eval function
    from the python matlab engine. THE DSPACE OBJECT MUST ALREADY EXISTS.

    Args:
        name: Name to indentify the new feature

    Returns:
        dsource.info string
    """

    # Transfer the numpy array to the already existing matlab workspace
    M = np.random.rand(1000, 28)
    engine.workspace["M"] = matlab.double(M.tolist())

    # Maybe do something like
    # send_matrix_to_matlab(engine, matrix, "name of the matrix for the matlab workspace")

    # Create instruction strings
    instr_feature_layout = "fl = dspace_features.FeatureLayout([1, 128], [], 1:128, [1, 128]);"
    instr_standard_features = f"f = dspace_features.StandardFeatures(M, '{name}', fl);"
    instr_add_features = "dsource.addFeatures(f);"

    # Make use of eval to add the feature to dsource
    engine.eval(instr_feature_layout, nargout=0)
    engine.eval(instr_standard_features, nargout=0)
    engine.eval(instr_add_features, nargout=0)

    engine.eval("dsource.info", nargout=0)


def send_matrix_to_matlab(engine: matlab.engine, matrix: np.ndarray, name_for_workspace: str) -> None:
    """
    TODO: Maybe not necessary.

    If a lot of methods using the engine are needed, it could be a
    good idea to wrap the matlab.engine object inside another engine
    class with all these functions as methods.
    """
    engine.workspace[name_for_workspace] = matlab.double(matrix.tolist())
