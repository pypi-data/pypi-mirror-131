# domain-check
A script running over all TLDs that fulfill specified requirements |check if `name.TLD` is still free. 
Using `dig` to check for availability. The list of all TLD-domains will be requested from `do.de` (not sponsored).  

## Options
| Parameter | Description | Default |
| --- | --- | --- |
| name | The domain name to check for | required input |
| \[-p\] \[--price\] | Max price for domain |  default=20.000 |
| \[-l\] \[--maxlen\] | Max length the TLD shall have | default=18 |
| \[-r\] \[--rate\] | Delay between whois-calls in seconds | default=0.2 |
| \[-f\] \[--file\] | File the available results are written to | default="./free.txt" |

## setup
Make sure that you've got the CLI-tool `dig` installed since it's the part required for checking the domain.
It should be part of `dnsutils`.   

After that install the package with pip:  
`pip install domain-check`  
Run it using a command like: 
`domain-check example -r 0.01 -f example.txt`  