# BatchTools
Scripts for use with Ansible batch.

## Usage Instructions

### AnsibleBatchGen.py
```
Usage: python3 AnsibleBatchGen.py <CT> [--no-script]
<CT>: Ticket ID
--no-script: Optional argument to print NODE information without generating script.
```

## Required Files

Ensure the following files are present in the `/tmp` directory:

1. **/tmp/numbers_`<CT>`**: Contains batches with host requirements.
   - Example: `B001,12`
2. **/tmp/todays_ct_dates.txt**: Scheduled start times for CTs.
   - Example: `123456789,18:00`
3. **/tmp/enable.node**: Lists enabled NODEs for batch distribution.
   - Example: `NODE1`
  
## Example of `--no-script`

```
$ python3 AnsibleBatchGen.py 12345 --no-script
NODE1 @ B037 B035 B081 B119 B047 B088 B130 B043 B110 B038 B093 @ 153
NODE2 @ B053 B049 B085 B002 B018 B048 B089 B003 B046 B112 B104 @ 153
NODE3 @ B070 B052 B086 B008 B021 B055 B091 B005 B050 B114 B108 @ 153
NODE4 @ B079 B056 B090 B009 B022 B057 B095 B010 B051 B116 B123 @ 153
NODE5 @ B080 B062 B097 B013 B027 B058 B096 B011 B060 B117 B125 @ 153
NODE6 @ B087 B065 B099 B014 B029 B059 B098 B012 B064 B120 B126 @ 153
NODE7 @ B103 B066 B100 B016 B031 B061 B102 B020 B068 B121 B129 @ 153
NODE8 @ B001 B017 B071 B101 B033 B063 B105 B025 B074 B122 B054 @ 152
NODE9 @ B004 B019 B073 B107 B034 B069 B106 B030 B082 B124 @ 141
NODE10 @ B006 B023 B075 B111 B040 B072 B109 B032 B084 B127 @ 141
NODE11 @ B007 B024 B076 B115 B042 B078 B113 B039 B092 B026 B045 @ 152
NODE12 @ B015 B028 B077 B118 B044 B083 B128 B041 B094 B036 B067 @ 152

```

### GenNumbers.py
```
Usage: python3 GenNumbers.py <total_batches> <total_hosts> <output_file_number>
```
File written to /tmp/numbers_`<output_file_number>`
