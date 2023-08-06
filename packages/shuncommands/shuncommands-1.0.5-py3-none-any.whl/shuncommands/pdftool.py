#!/usr/bin/env python3

from pathlib import Path

import click
from pikepdf import Pdf


@click.group()
@click.version_option(None, '-v', '--version')
@click.help_option('-h', '--help')
def ctx():
    '''
    \b
    PDF file をあれやこれやしたいがためのコマンド
    '''


@ctx.command()
@click.version_option(None, '-v', '--version')
@click.help_option('-h', '--help')
@click.option('password', '-p',
              help='decrypt password',
              prompt=True,
              hide_input=True)
@click.option('--output', '-o',
              help='output decrypt pdf filename [default: <pdffile>.unlock.pdf]',  # noqa: E501
              type=click.Path())
@click.option('--force', '-f',
              help='<output> override',
              is_flag=True)
@click.argument('pdffile',
                required=True,
                type=click.Path(exists=True))
def unlock(pdffile, output, password, force):
    '''
    パスワード付きPDFファイルを、パスワードなしPDFファイルにコピーする
    '''
    click.echo(f'input pdf file: {pdffile}')
    lockpdf = Pdf.open(pdffile, password=password)
    unlockpdf = Pdf.new()
    unlockpdf.pages.extend(lockpdf.pages)
    if output is None:
        output = Path(pdffile).with_suffix('.unlock.pdf')
    else:
        output = Path(output)
    if output.exists() or not force:
        click.confirm(f'{output} is exists. Do you want to override?',
                      default=True,
                      abort=True,
                      show_default=True)

    unlockpdf.save(output)
    click.echo(f'output pdf file: {output}')
