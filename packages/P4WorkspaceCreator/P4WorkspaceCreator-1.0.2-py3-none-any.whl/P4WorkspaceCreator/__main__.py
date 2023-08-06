import sys

if __name__ == "__main__":
    from P4WorkspaceCreator.WorkspaceCreator import main as _main
    sys.exit(_main(sys.argv[1:]))
