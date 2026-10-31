![Banner](banner.png)

# dm-data-field-shuffler
Shuffles the order of fields within each data record. This breaks simple field-order-dependent attacks and analysis without altering the individual field values. - Focused on Tools designed to generate or mask sensitive data with realistic-looking but meaningless values

## Install
`git clone https://github.com/ShadowGuardAI/dm-data-field-shuffler`

## Usage
`./dm-data-field-shuffler [params]`

Naming the output file as the input file is refused at exit 1 before any file is opened. An empty input file exits 1 with the line `Input file is empty.`, whether or not the header flag is given, and writes no output.

## Parameters
- `-h`: Show help message and exit
- `-H`: Treat the first row as a header and preserve it.

## License
Copyright (c) ShadowGuardAI
