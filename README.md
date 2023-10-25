#Get variables
Get telegram API ID and API Hash:

https://core.telegram.org/api/obtaining_api_id

#Variables encryption (for Windows) [optional]
It's strongly recommended encrypting your variables. From PowerShell:
> "P@ssword1" | ConvertTo-SecureString -AsPlainText -Force | ConvertFrom-SecureString

https://www.pdq.com/blog/secure-password-with-powershell-encrypting-credentials-part-1/

#Environment preparation
##Easy
- Install Python 3.11:

https://www.python.org/downloads/release/python-3115/

- Install from repository directory:

> pip install -e .
 
- Set environment variables:
  
  API_HASH: %api_hash%
  
  API_ID: %api_id%
  
  CHANNEL_NAME: %channel_name%


##Preferred
- Install Miniconda

https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html
  
- Create environment with .yml file from env folder:
> conda env create -f parser_example_env.yml

- Activate environment:
> activate parser_example_311
 
- In activated environment install from repository directory

> pip install -e .

- Set environment variables:
  
  API_HASH: %api_hash%
  
  API_ID: %api_id%
  
  CHANNEL_NAME: %channel_name%

# Script usage

> python -m parser messages
> 
> python -m parser messages -t "tag1,tag2" -s 01/01/2023 -e 16/7/2023

or
> python -m parser tags

All environment variables could be overloaded if needed.
Also custom parameters could be set to filter messages by tags (if any of tags found message will be picked up) and/or date.

>python -m parser --help
> 
>positional arguments:
>
> {messages,tags}
>options:
>
> -h, --help            show this help message and exit
 >
> -hash, --api_hash API_HASH
>
> -id, --api_id API_ID
> 
>  -c, --channel_name CHANNEL_NAME
>
>  --debug               Run program in debug mode.
 
 
>python -m parser messages --help
>
>options:
> 
>  -h, --help            show this help message and exit
>
>  -t, --tags TAGS  
> Put tag names in double quotes ("tag") separated with commas ("tag1,tag2,tag3")
>
>  -s, --start START
> 
>   Date from which messages should be processed. Date format dd/mm/yyyy.
>
>  -e, --end END     
> End date to which messages should be processed. Date format dd/mm/yyyy.


Output CSV files will be generated and stored under OUTPUT directory in repository folder.

#Pay attention
- Sessions termination

https://github.com/LonamiWebs/Telethon/issues/4051

https://stackoverflow.com/questions/75619803/telegram-account-needs-to-be-confirmed-every-time-when-using-telethon

- FloodWaitError due to 200 limit:

https://stackoverflow.com/questions/73230613/is-there-a-risk-that-get-input-entity-of-telethon-will-also-exceed-telegram

https://limits.tginfo.me/en

#Tag pattern

Matches Unicode word characters; this includes alphanumeric characters (as defined by str.isalnum()) as well as the underscore (_). If the ASCII flag is used, only [a-zA-Z0-9_] is matched.
Also included [. - , :]
