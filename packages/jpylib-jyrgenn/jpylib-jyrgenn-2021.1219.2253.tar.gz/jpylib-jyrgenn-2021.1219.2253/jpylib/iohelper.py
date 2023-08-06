import os
import sys

def all_input_lines(fnames=[], cont_err=False):
    """Like Perl's diamond operator <>, return lines from files or stdin.

    (Generator) If fnames is empty, return lines from stdin, otherwise
    lines from the named files, in succession. The file name "-" stands
    for stdin. Typically, something like sys.argv[1:] would be passed
    as an argument. If cont_err is true, continue after an error,
    printing an error message. If cont_err is a callable, call it with
    the file name and the exception on error.
    """
    # The following looks like a needless duplication of code. But in the
    # spirit of "it is more important for the interface to be simple than the
    # implementation", it must be like this. Factoring out the reading or the
    # exception handling would make the resulting exception stack more
    # complicated, which I want to avoid. Also, I want it to read stdin from
    # sys.stdin so I can easier redirect the input for testing.
    if not fnames:
        fnames = ["-"]
    for fname in fnames:
        try:
            if fname == "-":
                for line in sys.stdin:
                    yield line
            else:
                with open(fname) as f:
                    for line in f:
                        yield line
        except Exception as e:
            if cont_err:
                if callable(cont_err):
                    cont_err(fname, e)
                else:
                    program = os.path.basename(sys.argv[0])
                    print(program+":", e, file=sys.stderr)
            else:
                raise e
