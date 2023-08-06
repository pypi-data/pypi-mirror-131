# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 - 2021 TU Wien.
#
# Invenio-Utilities-TUW is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Management commands for files."""

import os
from collections import defaultdict

import click
from flask.cli import with_appcontext
from invenio_access.permissions import system_identity
from invenio_db import db
from invenio_files_rest.models import Location, ObjectVersion

from ..utils import get_record_service
from .options import option_pid_type, option_pid_value_optional
from .utils import convert_to_recid


def remove_file(file_path, max_rmdir_depth=3):
    """Remove the file and directories in its path that just became empty."""
    os.remove(file_path)
    path = os.path.dirname(file_path)
    depth = 0

    # only delete directories until the maximum rmdir depth is hit, or the
    # directory contains files, or we hit a permission error
    while depth < max_rmdir_depth and not os.listdir(path):
        try:
            os.rmdir(path)
        except PermissionError:
            break

        path, _ = os.path.split(path)
        depth += 1


def get_orphaned_files(location):
    """Get a list of files in the given Location that aren't referenced in the DB."""
    # see which files are on disk at the given location
    all_files = []
    for (p, _, files) in os.walk(location.uri):
        all_files += [os.path.join(p, f) for f in files]

    # filter out those files that invenio has knowledge about
    for bucket in location.buckets:
        for obj in bucket.objects:
            if obj.file and obj.file.uri in all_files:
                # an object_version without attached file_instance
                # likely denotes a soft-deleted file
                all_files.remove(obj.file.uri)

    return all_files


@click.group()
def files():
    """Management commands for files."""


@files.group("deleted")
def deleted():
    """Management commands for soft-deleted files."""


@deleted.command("list")
@option_pid_value_optional
@option_pid_type
@with_appcontext
def list_deleted_files(pid, pid_type):
    """List files that have already been soft-deleted.

    Optionally, this operation can be restricted to the bucket associated with a draft
    (via its PID).
    """
    recid = convert_to_recid(pid, pid_type) if pid else None
    service = get_record_service()
    identity = system_identity

    # if a PID was specified, limit the cleaning to this record's bucket
    marked_as_deleted = ObjectVersion.query.filter_by(file_id=None, is_head=True)
    if recid is not None:
        draft = service.read_draft(id_=recid, identity=identity)._record
        marked_as_deleted = marked_as_deleted.filter_by(bucket=draft.files.bucket)

    # hard-delete all soft-deleted ObjectVersions
    file_instances = defaultdict(set)
    for dov in marked_as_deleted.all():
        for ov in ObjectVersion.get_versions(dov.bucket, dov.key).all():
            if ov.file is not None:
                file_instances[ov.key].add(ov.file)

    # delete the associated FileInstances, and remove files from disk
    for key in file_instances:
        for fi in file_instances[key]:
            click.secho(f"{key}\t{fi.uri}", fg="green")

    db.session.commit()


@deleted.command("clean")
@click.confirmation_option(
    prompt="are you sure you want to permanently remove soft-deleted files?"
)
@option_pid_value_optional
@option_pid_type
@with_appcontext
def hard_delete_files(pid, pid_type):
    """Hard-delete files that have already been soft-deleted.

    Optionally, this operation can be restricted to the bucket associated with a draft
    (via its PID).
    """
    recid = convert_to_recid(pid, pid_type) if pid else None
    service = get_record_service()
    identity = system_identity

    # if a PID was specified, limit the cleaning to this record's bucket
    marked_as_deleted = ObjectVersion.query.filter_by(file_id=None, is_head=True)
    if recid is not None:
        draft = service.read_draft(id_=recid, identity=identity)._record
        marked_as_deleted = marked_as_deleted.filter_by(bucket=draft.files.bucket)

    # hard-delete all soft-deleted ObjectVersions
    file_instances = defaultdict(set)
    for dov in marked_as_deleted.all():
        for ov in ObjectVersion.get_versions(dov.bucket, dov.key).all():
            ov.remove()
            if ov.file is not None:
                file_instances[ov.key].add(ov.file)

    # delete the associated FileInstances, and remove files from disk
    for key in file_instances:
        for fi in file_instances[key]:
            try:
                storage = fi.storage()
                fi.delete()
                storage.delete()
                click.secho(f"{key}\t{fi.uri}", fg="red")

            except Exception as error:
                click.secho(
                    f"cannot delete file '{fi.uri}': {error}", fg="yellow", err=True
                )

    db.session.commit()


@files.group("orphans")
def orphans():
    """Management commands for unreferenced files.

    Orphaned files are those that are still present in the storage, but are not
    referenced by any Location's buckets anymore.
    """


@orphans.command("list")
@with_appcontext
def list_orphan_files():
    """List existing files that aren't referenced in Invenio anymore."""
    for loc in Location.query.all():
        # we only know how to handle directories on the file system for now
        if os.path.isdir(loc.uri):
            click.echo(f"location: {loc.name}")
        else:
            click.secho(
                f"warning: location '{loc.name}' is not a path: {loc.uri}",
                fg="yellow",
            )

        for fp in get_orphaned_files(loc):
            click.echo(f"  {fp}")


@orphans.command("clean")
@click.confirmation_option(
    prompt="are you sure you want to permanently remove orphaned files?"
)
@with_appcontext
def clean_files():
    """Delete existing files that aren't referenced in Invenio anymore."""
    for loc in Location.query.all():
        # we only know how to handle directories on the file system for now
        if not os.path.isdir(loc.uri):
            click.secho(
                f"don't know how to handle location '{loc.name}': skipping",
                fg="yellow",
                err=True,
            )
            continue

        for fp in get_orphaned_files(loc):
            try:
                remove_file(fp)
                click.secho(fp, fg="green")

            except PermissionError:
                click.secho(fp, fg="yellow", err=True)
