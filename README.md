# PIUS: The PGP Individual UID Signer

## Introduction

PIUS started life as a group of bad shell scripts I had thrown together through
the years after going to various PGP keysigning parties. These scripts
automated various bits and pieces of signing various keys and UIDs, but fell
short of actually making it a mostly painless process.

Finally I decided to sit down and combine all these shell scripts into a single
unified utility to make signing individual UIDs on a multitude of keys as
painless as possible. Since this was going to be mostly forking off gpg
instances, it seemed like shell was the way to go. However, after dealing with
gpg and it's "API" for a while, I quickly realized that was not going to be the
best course of action. Since I wanted an excuse to write more python, instead
of my usual perl, I decided to write this in python.

The original version heavily used the pexpect module for various reasons: (1) I
wanted to be able to let the user enter the passphrase directly into gpg for
security reasons, (2) Using the --{command,passphrase,status}-fd options turned
not to be not that well documented and not work the way the documentation
suggested.

This method quickly showed itself to be very fragile. So, I managed to bend gpg
to my will without using pexpect, and the only thing left that uses pexpect is
the 'interactive' mode, which will probably one day go away if gpg-agent
becomes reliable enough.


## Usage

The most common way to use PIUS is with a keyring from a keysigning party, like
this:

```
$ pius -A -a -s <your_keyid> -r <path_to_keyring> -m <your_email>
```

For every key (`-A`) on the keyring (`-r`) this will prompt you to verify the
fingerprint and choose a signing level. Then, if you tell it to, it will sign
all UIDs on <keyid>, and export one copy of the for each UID with only that UID
signed. Each one will then be encrypt-emailed off to the email address in the
UID (`-m`). The `-a` tells it to use gpg-agent and `-s` tells it which key to
sign with.

There are a variety of other options that you may want:
  * customize the tmpdir and outdir directories (-t and -o respectively)
  * encrypt the outfiles to <filename>_ENCRYPTED.asc (-e)
  * import the unsigned keys to the default keyring (-I)
  * verbose mode (-v)
  * customize mail hostname and port (-H and -P respectively)
  * customize the email message (-M)
  * don't use PGP/Mime in the email (-O, implies -e)
  * specify a SMTPAUTH or STARTTLS for SMTP (-u and -S)

And more! See the '-h' option for more.


## Security Implications

The default mode for pius, starting in 2.0.0 is 'cache_passphrase' mode. This
means that pius will ask you for your passphrase at startup, verify this
passphrase is correct, and then feed it GnuPG everytime it needs it. The
passphrase is stored in memory and only for the life of the execution of pius.
For most users this should be relatively safe. However, it is worth noting that
if you are on a machine whose system administrators you don't trust, there is a
small danger of them reading this memory while pius is running.

There are two alternatives for people not comfortable with this. The first is to
use the agent mode. By specifying -a, pius will ask gpg to get the passphrase
from an gpg-agent. You will need to have your gpg-agent setup and running.
However, gpg-agent can be rather flaky, so we recommend you pre-seed by doing
something that requires your private keys so it can cache your keys before you
run pius.

Finally we have 'interactive mode' which can be entered using -i. This will use
pexpect to handle most of the signing interactions and then drop you into the
'gpg --edit-key' shell whenever gpg needs a passphrase. Using this you can enter
your passphrase directly into gpg. This mode has two main disadvantages. The
first is that the pexpect code is quite fragile, and the second is that you'll
have to type your passphrase for every key-UID combination.


## Sending Emails

When PIUS emails out keys it BCC's you, so you will get a copy of every email
sent out. If you would like to see what is going to be sent and not have it
sent, you can either do:

```
  $ pius -T
```

To have PIUS dump the text of the default email body, or you can use the -n
option to forcefully override the TO in the envelope of the email. When doing
this *only* the address specified as an argument to `-n` will get the email.

If you want to see the email sent when not using PGP/Mime then try:

```
  $ pius -T -O
```

If you want to customize this message you can do so with the -M option. Note
that you may use python's named variable interpolation syntax here to have pius
fill in email (the email in the UID, i.e. the recipient), keyid (of the key that
was signed), and signer (the keyid used to sign, i.e. your keyid). For example,
you can simply include "%(keyid)s" (without the quotes) to get the keyid.


## License

PIUS is released under the GNU Public License v2 and is Copyright `Phil Dibowitz
<phil@ipom.com>`.


## Config File

You can specify options you'd like to always use in a ~/.pius file. The format
of this file is option=value. The "=value" part is obviously not required for
options that don't have a value. An example might be:

```
mail=you@sample.com
tmp-dir=/home/you/pius/tmp
```

Pius will except both `=`, `:`, or whitespace as a separator, and will handle
extra whitespace around any separator.


Phil Dibowitz

phil@ipom.com


vim:shiftwidth=2:tabstop=2:expandtab:textwidth=80:softtabstop=2:ai:
