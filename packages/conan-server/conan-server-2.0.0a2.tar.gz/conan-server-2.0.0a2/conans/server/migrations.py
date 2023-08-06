import os
import shutil

from conans import DEFAULT_REVISION_V1
from conans.migrations import Migrator
from conans.server.revision_list import RevisionList
from conans.server.store.server_store import REVISIONS_FILE, SERVER_PACKAGES_FOLDER
from conans.util.files import list_folder_subdirs, mkdir, save
from conans.util.log import logger


class ServerMigrator(Migrator):

    def __init__(self, conf_path, store_path, current_version, force_migrations):
        self.force_migrations = force_migrations
        self.store_path = store_path
        super(ServerMigrator, self).__init__(conf_path, current_version)

    def migrate_to_revisions_layout(self):
        # .conan/data/lib/1.0/user/channel/export/*
        # .conan/data/lib/1.0/user/channel/0/export/*

        # .conan/data/lib/1.0/user/channel/package/*
        # .conan/data/lib/1.0/user/channel/0/package/*

        # .conan/data/lib/1.0/user/channel/package/XXX/*
        # .conan/data/lib/1.0/user/channel/0/package/XXX/0/*
        if not self.force_migrations:
            print("**********************************************")
            print("*                                            *")
            print("*      ERROR: STORAGE MIGRATION NEEDED!      *")
            print("*                                            *")
            print("**********************************************")
            msg = "A migration of your storage is needed, please backup first the storage " \
                  "directory and run:\n\n$ conan_server --migrate\n\n"
            logger.error(msg)
            print(msg)
            exit(3)  # Gunicorn expects error code 3 to stop retrying booting the worker

        print("**********************************************")
        print("*                                            *")
        print("*       MIGRATION IN PROGRESS                *")
        print("*                                            *")
        print("**********************************************")
        subdirs = list_folder_subdirs(basedir=self.store_path, level=4)
        for subdir in subdirs:
            base_dir = os.path.join(self.store_path, subdir)
            for export_or_package in os.listdir(base_dir):
                the_dir = os.path.join(base_dir, export_or_package)
                dest_dir = os.path.join(base_dir, DEFAULT_REVISION_V1)
                mkdir(dest_dir)
                print("Moving '%s': %s" % (subdir, export_or_package))
                shutil.move(the_dir, dest_dir)

            rev_list = RevisionList()
            rev_list.add_revision(DEFAULT_REVISION_V1)
            save(os.path.join(base_dir, REVISIONS_FILE), rev_list.dumps())

            packages_dir = os.path.join(self.store_path, subdir, DEFAULT_REVISION_V1,
                                        SERVER_PACKAGES_FOLDER)

            if not os.path.exists(packages_dir):
                print("NO PACKAGES")
                continue
            for pid in os.listdir(packages_dir):
                package_dir = os.path.join(packages_dir, pid)
                mkdir(os.path.join(package_dir, DEFAULT_REVISION_V1))
                print(" - Package '%s'" % pid)
                for item in os.listdir(package_dir):
                    if item == DEFAULT_REVISION_V1:
                        continue
                    origin_path = os.path.join(package_dir, item)
                    dest_path = os.path.join(package_dir, DEFAULT_REVISION_V1, item)
                    mkdir(dest_dir)
                    shutil.move(origin_path, dest_path)
                rev_list = RevisionList()
                rev_list.add_revision(DEFAULT_REVISION_V1)
                save(os.path.join(package_dir, REVISIONS_FILE), rev_list.dumps())
        print("**********************************************")
        print("*                                            *")
        print("*       MIGRATION COMPLETED!                 *")
        print("*                                            *")
        print("**********************************************")
