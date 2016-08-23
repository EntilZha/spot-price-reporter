from datetime import datetime
from datetime import timedelta
import os
from os import path
import click
from spot_reporter import reporting, slack


@click.command()
@click.option('--action', '-a', multiple=True, type=click.Choice(['email', 'slack']),
              help='Determine if/how to send aws pricing report')
@click.option('--output-dir', type=str, default='/tmp/spot-reporter',
              help='What directory to output files to, by default /tmp/spot-reporter')
@click.option('--end-time', type=str, default=None, help='Last time to check spot price for')
@click.option('--region', type=str, default=None,
              help='AWS region, by default uses the environment')
@click.option('--skip-generation', is_flag=True, help='Skip file generation')
@click.argument('instance_types', nargs=-1, required=True)
def cli(action, output_dir, end_time, region, skip_generation, instance_types):
    print('Running spot price reporter')
    daily_path = path.join(output_dir, 'aws_spot_price_daily.png')
    weekly_path = path.join(output_dir, 'aws_spot_price_weekly.png')
    if end_time is None:
        stop_datetime = datetime.now()
    else:
        stop_datetime = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S')
    if not skip_generation:
        print('Getting AWS data')
        daily_data = reporting.get_spot_price_data(
            instance_types,
            start_time=stop_datetime - timedelta(days=1),
            end_time=stop_datetime,
            region=region
        )
        weekly_data = reporting.get_spot_price_data(
            instance_types,
            start_time=stop_datetime - timedelta(days=7),
            end_time=stop_datetime,
            region=region
        )

        if not path.exists(output_dir):
            os.makedirs(output_dir)

        print('Creating plots')
        reporting.create_plot(daily_data, daily_path)
        reporting.create_plot(weekly_data, weekly_path)

    if 'slack' in action:
        print('Uploading and messaging slack')
        slack.notify(daily_path, weekly_path, stop_datetime)


if __name__ == '__main__':
    cli()
