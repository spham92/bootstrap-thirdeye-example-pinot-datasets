# Prerequisites

This script requires python3 to be installed on your machine. You can either use brew or https://www.python.org/downloads/.

# Setup

```commandline
gh repo clone spham92/bootstrap-thirdeye-example-pinot-datasets
cd bootstrap-thirdeye-example-pinot-dataset
python3 -m venv venv
source venv/bin/activate
pip install -r reuquirements.txt
```

# Usage
Once setup ensure you have run `source venv/bin/activate` from the script project

Now change into ThirdEye's repo's example directory
```commandline
cd ~/projects/thirdeye/examples

python3 [PATH TO THE main.py script]
```