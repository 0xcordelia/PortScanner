# Port Scanner

A simple, multithreaded port scanner written in Python.

## Features

- Fast multithreaded scanning
- Configurable port ranges
- JSON output support
- Quiet mode for automation
- Common ports preset

## Usage

```bash
# Scan common ports
python3 scanner.py google.com

# Scan specific port range
python3 scanner.py -p 1-1000 example.com

# JSON output
python3 scanner.py -o json target.com

# Quiet mode with custom timeout
python3 scanner.py -q -t 2 target.com

# Custom thread count
python3 scanner.py --threads 100 -p 80-443 target.com
```

## Options

- `host`: Target hostname or IP address
- `-p, --ports`: Port range (default: common ports)
- `-t, --timeout`: Connection timeout in seconds (default: 1)
- `--threads`: Number of threads (default: 50)
- `-o, --output`: Output format - text or json (default: text)
- `-q, --quiet`: Quiet mode - only show results

## Examples

Scan common ports on localhost:
```bash
python3 scanner.py localhost
```

Fast scan of web ports:
```bash
python3 scanner.py -p 80-443 --threads 200 example.com
```

JSON output for automation:
```bash
python3 scanner.py -o json -q example.com | jq '.open_ports'
```