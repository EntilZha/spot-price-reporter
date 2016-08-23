import subprocess
from datetime import datetime
from datetime import timedelta
import json
import pandas as pd
import seaborn as sns
import matplotlib


def get_spot_price_data(instance_types, start_time=None, end_time=None, region=None):
    """
    Fetches the current spot price history for the given instances types and date range for the
    specified region. If the region is not specified then it falls back to the defaults set by the
    environment.

    :param instance_types: list(str), list of instances to get price for
    :param start_time: starting time
    :param end_time: ending time
    :param region: region string, if None defaults
    :return: json dataset with correctly formatted columns
    """

    if region is not None:
        command = ['aws', '--region', region, 'ec2', 'describe-spot-price-history']
    else:
        command = ['aws', 'ec2', 'describe-spot-price-history']
    options = []

    if len(instance_types) < 1:
        raise ValueError('Expected instance_types to have at least one instance type')

    options.extend(['--instance-types'] + list(instance_types))

    if start_time is not None:
        options.extend(['--start-time', start_time.strftime('%Y-%m-%dT%H:%M:%S')])

    if end_time is not None:
        options.extend(['--end-time', end_time.strftime('%Y-%m-%dT%H:%M:%S')])

    output = subprocess.run(
        command + options,
        check=True,
        stdout=subprocess.PIPE
    )
    j = json.loads(output.stdout.decode('utf-8'))
    data = j['SpotPriceHistory']
    for r in data:
        r['SpotPrice'] = float(r['SpotPrice'])
        ts = datetime.strptime(r['Timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
        r['DateTime'] = ts
        r['Timestamp'] = ts.timestamp()

    return data


def create_plot(json_data, output):
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    all_data = pd.DataFrame(json_data)
    df = all_data[all_data['ProductDescription'] == 'Linux/UNIX']
    df = df.drop_duplicates(subset=['DateTime', 'AvailabilityZone', 'InstanceType'])
    x_min = df['DateTime'].min()
    x_max = df['DateTime'].max()
    border_pad = (x_max - x_min) * 5 / 100

    g = sns.FacetGrid(
        df,
        col='InstanceType',
        hue='AvailabilityZone',
        xlim=(x_min - border_pad, x_max + border_pad),
        legend_out=True,
        size=10,
        palette="Set1"
    )
    g.map(plt.scatter, 'DateTime', 'SpotPrice', s=4).add_legend()
    plt.subplots_adjust(top=.9)
    g.fig.suptitle('AWS Spot Prices between {start} and {end}'.format(start=x_min, end=x_max))
    g.savefig(output, format='png')
