'''
Created Date: Sunday, December 19th 2021
Author: Sachin Srivastava

Copyright (c) 2021 Sachin Srivastava
'''

from P4 import P4 as Perforce
from P4 import P4Exception
import os
import sys
import tempfile
import logging
import argparse
from socket import gethostname
from stat import S_IWUSR, S_IREAD

DEFAULT_PORT = "perforce:1666"

VIEW = "View"
ROOT = "Root"
HOST = 'Host'
OWNER = "Owner"
DESCRIPTION = "Description"

USER = "user"
PASSWORD = "password"
CLIENT = "client"
PORT = "port"
ROOT = "root"
SPEC_FILE = "spec_file"
PLACE_HOLDER = "placeholder"
CUSTOM_LOGGER = "logger"

main_logger = logging.getLogger(__name__)


def scan_args(args=None):

    parser = argparse.ArgumentParser(
        description="Script to create perforce workspace using the spec file (cws)")

    parser.add_argument(
        '-u', '--user', help='Perforce user name', required=True)

    parser.add_argument('-p', '--password',
                        help="Perforce password", required=True)

    parser.add_argument('-port',
                        '--port', help="Perforce port address", default=DEFAULT_PORT)

    parser.add_argument(
        '-c', '--client', help="Client name which will be used to create workspace", required=True)

    parser.add_argument(
        '-r', '--root', help="Workspace root path", required=True)

    parser.add_argument(
        '-s', '--spec', help="Spec file path in depot", required=True)

    parser.add_argument(
        '-l', '--placeholder', help="Place holder used in the spec file e.g '<ClientName>'", required=True, default="<ClientName>")

    result = parser.parse_args(args)

    return result.user, result.password, result.port, result.client, result.root, result.spec, result.placeholder


def create(p4, root_path, client_name, spec_file_path, place_holder, logger):
    """
        This will create workspace using the provided workspace root path, client name i.e., workspace name,
        spec file and placeholder value in the spec file which will be replaced by client name (workspace name)
    """
    try:
        spec_file = spec_file_path.split("/")[-1]

        temp_spec_output_path = os.path.join(tempfile.gettempdir(), spec_file)

        logger.info(f"Output Path: {temp_spec_output_path}")

        p4.run("print", "-o", temp_spec_output_path,
               spec_file_path, logger=logger)

        p4_client = p4.fetch_client(client_name)

        with open(temp_spec_output_path, "r") as f:
            spec_mapping_lines = []
            for spec_line in f.readlines():
                spec_line = spec_line.strip()
                if not spec_line.startswith("#") and len(spec_line) > 0:
                    spec_mapping_lines.append(
                        spec_line.replace(place_holder, client_name))

        p4_client[OWNER] = p4.user.upper()
        p4_client[VIEW] = spec_mapping_lines
        p4_client[ROOT] = root_path
        p4_client[HOST] = gethostname()
        p4_client[DESCRIPTION] = f"Created by {p4_client[OWNER]} via script"

        p4.save_client(p4_client, logger=logger)

        logger.info(
            f"Finished processing Workspace: {client_name} under root path: {root_path}.")

        sys.exit(0)

    except (P4Exception, Exception) as ex:
        error_msg = f"Unable to create workspace {client_name} using {spec_file_path}", ex
        logger.error(error_msg)
        sys.exit(1)

    finally:
        try:
            p4.disconnect()
        except P4Exception:
            logger.error("Unable to disconnect the perforce connection.")

        if os.path.exists(temp_spec_output_path):
            logger.info(
                f"Deleting temporary spec file created in the temp directory {temp_spec_output_path}")
            try:
                os.chmod(temp_spec_output_path, S_IWUSR | S_IREAD)
                os.remove(temp_spec_output_path)
            except PermissionError:
                logger.info(
                    f"Unable to remove the temporary spec file {temp_spec_output_path} due to permission error")
            except Exception as ex:
                error_msg = f"Unable to create workspace {client_name} using {spec_file_path}", ex
                logger.info(error_msg)


def intialize_and_create_workspace(**kargs):
    """
        [Required keyword arguments user, password, port, client, root, spec_file, placeholder, logger (optional)]
    """

    try:
        p4_user = kargs[USER]
        p4_password = kargs[PASSWORD]
        client_name = kargs[CLIENT]
        root_path = kargs[ROOT]
        spec_file_path = kargs[SPEC_FILE]

        port = DEFAULT_PORT
        if PORT in kargs:
            port = kargs[PORT]

        place_holder = "<ClientName>"

        if PLACE_HOLDER in kargs:
            place_holder = kargs[PLACE_HOLDER]

        logger = main_logger

        if CUSTOM_LOGGER in kargs:
            logger = kargs[CUSTOM_LOGGER]

        # Set the P4 Client to blank so it should not take any default Workspace (P4CLIENT)
        os.environ["P4CLIENT"] = ""

        logger.info(
            f"Creating/Recreating workspace {client_name} with the spec file {spec_file_path} at root path {root_path}")

        p4 = Perforce(logger=logger)

        p4.user = p4_user

        p4.password = p4_password

        p4.client = ""

        p4.port = port

        p4.connect()                 # Connect to the Perforce server
        p4.run_login()               # Logging into Helix server ticket-based authentication

        create(p4, root_path, client_name,
               spec_file_path, place_holder, logger)

    except P4Exception as ex:
        logger.error("Unable to login to the perforce server.")

        for e in p4.errors:            # Display errors
            logger.error(e)

        if len(p4.errors) == 0:
            logger.error(ex.value)
            logger.error("Check your connection (Internet/VPN).")
        sys.exit(1)

    except Exception as ex:
        error_msg = "Unable to create workspace due to an exception", ex
        logger.error(error_msg)
        sys.exit(1)


def main(args):
    user, password, port, client, root, spec, placeholder = scan_args(args)

    logger = main_logger

    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler(sys.stderr)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    if user == None or password == None or client == None or spec == None:
        logger.error(
            f"Unable to create workspace as invalid arguments passed: User: {user}, Client: {client}, Root: {root}, Spec File: {spec}, Placeholder: {placeholder}")

    intialize_and_create_workspace(user=user, password=password, port=port, client=client,
                                   root=root, spec_file=spec, placeholder=placeholder, logger=logger)


if __name__ == "__main__":
    main(sys.argv[1:])
