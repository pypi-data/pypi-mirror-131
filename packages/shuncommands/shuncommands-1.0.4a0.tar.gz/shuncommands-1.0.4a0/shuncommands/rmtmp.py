#!/usr/bin/env python3

from datetime import datetime, timedelta
from pathlib import Path
from shutil import rmtree

import click
from gitignore_parser import parse_gitignore


@click.command(no_args_is_help=True)
@click.option('-q', '--quiet',
              is_flag=True,
              help='quiet output')
@click.option('--dry-run',
              is_flag=True)
@click.option('-d', '--day',
              type=click.IntRange(0),
              default=3,
              help='削除対象となる期日',
              show_default=True)
@click.argument('targetdir',
                type=click.Path(exists=True))
def ctx(targetdir, day, dry_run, quiet):
    '''
    tmpディレクトリの中身お掃除君

    \b
    <TARGETDIR>で指定されたディレクトリの中身をせっせとお掃除してくれるかわいいやつ。
    自分がよく ~/document/tmp/ とか雑にディレクトリ作ってしまうので、それのお掃除用に生まれた

    <TARGETDIR>/.rmtmpignore のファイルに gitignore と同様の書式でファイルを指定することで、
    削除対象から明示的に外すことができる。
    '''
    target = Path(targetdir).expanduser()
    if not quiet:
        click.echo(f'target is [{target}]')
    rmtmpignore = Path(target, '.rmtmpignore')
    target_files = get_files(target)
    if rmtmpignore.exists() and not quiet:
        click.echo(f'find [{rmtmpignore}]')
    target_files = filter_files(target_files, day, rmtmpignore)
    rm_files(target_files, dry_run, quiet)


def get_files(target):
    files = [f for f in target.iterdir()]
    return files


def filter_files(target_files, day, rmtmpignore):
    files = []
    matches = None
    if rmtmpignore.exists():
        matches = parse_gitignore(rmtmpignore)
        try:
            target_files.pop(target_files.index(rmtmpignore))
        except Exception as error:
            click.echo(f'WARN: {error}', err=True)
    for file in target_files:
        if matches is not None and matches(file):
            continue
        mtime = datetime.fromtimestamp(file.stat().st_mtime)
        today = datetime.now()
        if today - mtime < timedelta(days=day):
            continue
        files.append(file)
    return files


def rm_files(target_files, dry_run, quiet):
    for file in target_files:
        if dry_run is True:
            click.echo(file)
        else:
            try:
                if not quiet:
                    click.echo(f'rm [{file}]')
                if file.is_dir():
                    rmtree(file)
                else:
                    file.unlink()
            except Exception as error:
                msg = f'{file} remove failur [{error}]'
                click.echo(msg, err=True)
