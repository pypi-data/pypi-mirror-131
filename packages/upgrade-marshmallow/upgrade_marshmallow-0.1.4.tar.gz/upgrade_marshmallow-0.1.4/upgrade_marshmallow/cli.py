import click

from upgrade_marshmallow import utils
from upgrade_marshmallow.upgrade import replace_as_metadata_kw


@click.group()
def main():
    pass


@main.command()
@click.argument('file')
@click.option('-d', '--destination', type=click.Path(),
              help='如果不指定输出文件，则覆盖输入文件')
@click.option('-i', '--indent', type=click.INT,
              help='输出文件的缩进空格',
              default=4)
def upgrade(file, destination, indent):
    destination = destination or file
    source_code = replace_as_metadata_kw(file, indent=indent)
    utils.output_file(source_code, destination)


@main.command()
def peek():
    raise NotImplementedError


if __name__ == '__main__':
    main()
