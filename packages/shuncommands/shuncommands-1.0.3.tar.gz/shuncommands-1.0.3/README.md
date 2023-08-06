# shuncommands
my usefull commands

# install

```
$ pip install shuncommands
```

# install commands

  * rmtmp
  * pdftool

# rmtmp Usage

```
Usage: rmtmp [OPTIONS] TARGETDIR

  tmpディレクトリの中身お掃除君

  <TARGETDIR>で指定されたディレクトリの中身をせっせとお掃除してくれるかわいいやつ。
  自分がよく ~/document/tmp/ とか雑にディレクトリ作ってしまうので、それのお掃除用に生まれた

  <TARGETDIR>/.rmtmpignore のファイルに gitignore と同様の書式でファイルを指定することで、
  削除対象から明示的に外すことができる。

Options:
  -q, --quiet              quiet output
  --dry-run
  -d, --day INTEGER RANGE  削除対象となる期日  [default: 3; x>=0]
  --help                   Show this message and exit.
```

# pdftool usage

```
Usage: pdftool [OPTIONS] COMMAND [ARGS]...

  PDF file をあれやこれやしたいがためのコマンド

Options:
  --help  Show this message and exit.

Commands:
  unlock  パスワード付きPDFファイルを、パスワードなしPDFファイルにコピーする
```
