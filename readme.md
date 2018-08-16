
# A html email compatibility issue between frameflow and Exchange

* Personal experience

* Not official

## So, what was the problem?

You may notice html email (in Exchange mailbox) comes from Frameflow sometimes a space inserted in the string, or a line break has been removed unexpectly.

If you looking into the source code of the html email, you can see some strange html tag like following,

```
<b r="">1111
 22222
```

However, if you double check the html content on SMTP server (in my case Postfix), the contents is always correct.

So, something wrong when sending html email from Postfix to Exchange

Dig more, if an email is sent by .Net API, like `Send-MailMessage` of PowerShell, the result is always right.

A simple guess is Frameflow isn't using .Net API to send emails, it might simply open SMTP service on TCP port 25 and write content instead.

That's where I am thinking the compatibility issue comes from.

## So, how to fix?

Apparently I can't or "don't want to" change how Frameflow works.

Turns out the SMTP (Postfix) server is my best option to make a fix.

Beautifully, Postfix is able to modify content before send emails out.

* http://www.postfix.org/FILTER_README.html

Follow the instruction from above URL to enable content filter.

In my case, I changed `/etc/postfix/master.cf` for following block to enable filter.

```
smtp      inet  n       -       n       -       -       smtpd
  -o content_filter=filter:dummy
------------------------------------------------------------------------------
filter    unix  -       n       n       -       10      pipe
  flags=Rq user=postfixfilter null_sender=
  argv=/var/spool/filter/content_filter.sh -f ${sender} -- ${recipient}
```

So, all emails will be sent to `content_filter.sh` and passed to `content_filter.py` to read and modify content.

The python script simply change the encoding of emails to `quoted-printable`, which Exchange happys.

## More?

Please turn SELinux off to debug the script, it takes some steps to run along with SELinux which will not be described here.
