import click


@click.command()
@click.option('-r', '--repo', help='repo name')
@click.argument('keyword')
def main(repo, keyword):
    print(repo, keyword)


if __name__ == '__main__':
    main()
