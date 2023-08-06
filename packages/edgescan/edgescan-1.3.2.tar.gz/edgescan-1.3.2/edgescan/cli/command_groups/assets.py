from typing import Optional
from edgescan.api.client import EdgeScan
from edgescan.constants import DEFAULT_INDENT, SORT_KEYS_BY_DEFAULT

import itertools
import json
import edgescan.cli.cli_helpers as cli
import collections
import ipaddress
import click


@click.group()
@click.pass_context
def assets(_):
    """
    Query or count assets.
    """
    pass


@assets.command()
@click.option('--asset-id', type=int, required=True)
@click.pass_context
def get_asset(ctx: click.Context, asset_id: int):
    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    asset = api.get_asset(asset_id)
    if asset:
        click.echo(asset.to_json())


@assets.command()
@click.option('--asset-ids')
@click.option('--asset-names')
@click.option('--asset-tags')
@click.option('--host-ids')
@click.option('--hostnames')
@click.option('--ip-addresses')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--alive/--dead', default=None)
@click.option('--vulnerability-ids')
@click.option('--vulnerability-names')
@click.option('--cve-ids')
@click.option('--min-asset-create-time')
@click.option('--max-asset-create-time')
@click.option('--min-asset-update-time')
@click.option('--max-asset-update-time')
@click.option('--min-next-assessment-time')
@click.option('--max-next-assessment-time')
@click.option('--min-last-assessment-time')
@click.option('--max-last-assessment-time')
@click.option('--min-last-host-scan-time')
@click.option('--max-last-host-scan-time')
@click.option('--min-host-last-seen-time')
@click.option('--max-host-last-seen-time')
@click.option('--min-vulnerability-create-time')
@click.option('--max-vulnerability-create-time')
@click.option('--min-vulnerability-update-time')
@click.option('--max-vulnerability-update-time')
@click.option('--min-vulnerability-open-time')
@click.option('--max-vulnerability-open-time')
@click.option('--min-vulnerability-close-time')
@click.option('--max-vulnerability-close-time')
@click.option('--limit', type=int)
@click.pass_context
def get_assets(
        ctx: click.Context,
        asset_ids: Optional[str],
        asset_names: Optional[str],
        asset_tags: Optional[str],
        host_ids: Optional[str],
        hostnames: Optional[str],
        ip_addresses: Optional[str],
        os_types: Optional[str],
        os_versions: Optional[str],
        alive: Optional[bool],
        vulnerability_ids: Optional[str],
        vulnerability_names: Optional[str],
        cve_ids: Optional[str],
        min_asset_create_time: Optional[str],
        max_asset_create_time: Optional[str],
        min_asset_update_time: Optional[str],
        max_asset_update_time: Optional[str],
        min_next_assessment_time: Optional[str],
        max_next_assessment_time: Optional[str],
        min_last_assessment_time: Optional[str],
        max_last_assessment_time: Optional[str],
        min_last_host_scan_time: Optional[str],
        max_last_host_scan_time: Optional[str],
        min_host_last_seen_time: Optional[str],
        max_host_last_seen_time: Optional[str],
        min_vulnerability_create_time: Optional[str],
        max_vulnerability_create_time: Optional[str],
        min_vulnerability_update_time: Optional[str],
        max_vulnerability_update_time: Optional[str],
        min_vulnerability_open_time: Optional[str],
        max_vulnerability_open_time: Optional[str],
        min_vulnerability_close_time: Optional[str],
        max_vulnerability_close_time: Optional[str],
        limit: Optional[int] = None):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    for asset in api.iter_assets(
        ids=cli.str_to_ints(asset_ids),
        names=cli.str_to_strs(asset_names),
        tags=cli.str_to_strs(asset_tags),
        host_ids=cli.str_to_ints(host_ids),
        hostnames=cli.str_to_strs(hostnames),
        ip_addresses=cli.str_to_strs(ip_addresses),
        os_types=cli.str_to_strs(os_types),
        os_versions=cli.str_to_strs(os_versions),
        alive=alive,
        vulnerability_ids=cli.str_to_ints(vulnerability_ids),
        vulnerability_names=cli.str_to_strs(vulnerability_names),
        cve_ids=cli.str_to_strs(cve_ids),
        min_asset_create_time=cli.str_to_datetime(min_asset_create_time),
        max_asset_create_time=cli.str_to_datetime(max_asset_create_time),
        min_asset_update_time=cli.str_to_datetime(min_asset_update_time),
        max_asset_update_time=cli.str_to_datetime(max_asset_update_time),
        min_next_assessment_time=cli.str_to_datetime(min_next_assessment_time),
        max_next_assessment_time=cli.str_to_datetime(max_next_assessment_time),
        min_last_assessment_time=cli.str_to_datetime(min_last_assessment_time),
        max_last_assessment_time=cli.str_to_datetime(max_last_assessment_time),
        min_last_host_scan_time=cli.str_to_datetime(min_last_host_scan_time),
        max_last_host_scan_time=cli.str_to_datetime(max_last_host_scan_time),
        min_host_last_seen_time=cli.str_to_datetime(min_host_last_seen_time),
        max_host_last_seen_time=cli.str_to_datetime(max_host_last_seen_time),
        min_vulnerability_create_time=cli.str_to_datetime(min_vulnerability_create_time),
        max_vulnerability_create_time=cli.str_to_datetime(max_vulnerability_create_time),
        min_vulnerability_update_time=cli.str_to_datetime(min_vulnerability_update_time),
        max_vulnerability_update_time=cli.str_to_datetime(max_vulnerability_update_time),
        min_vulnerability_open_time=cli.str_to_datetime(min_vulnerability_open_time),
        max_vulnerability_open_time=cli.str_to_datetime(max_vulnerability_open_time),
        min_vulnerability_close_time=cli.str_to_datetime(min_vulnerability_close_time),
        max_vulnerability_close_time=cli.str_to_datetime(max_vulnerability_close_time),
        limit=limit,
    ):
        click.echo(asset.to_json())


@assets.command()
@click.option('--asset-ids')
@click.option('--asset-names')
@click.option('--asset-tags')
@click.option('--host-ids')
@click.option('--hostnames')
@click.option('--ip-addresses')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--alive/--dead', default=None)
@click.option('--vulnerability-ids')
@click.option('--vulnerability-names')
@click.option('--cve-ids')
@click.option('--min-asset-create-time')
@click.option('--max-asset-create-time')
@click.option('--min-asset-update-time')
@click.option('--max-asset-update-time')
@click.option('--min-next-assessment-time')
@click.option('--max-next-assessment-time')
@click.option('--min-last-assessment-time')
@click.option('--max-last-assessment-time')
@click.option('--min-last-host-scan-time')
@click.option('--max-last-host-scan-time')
@click.option('--min-host-last-seen-time')
@click.option('--max-host-last-seen-time')
@click.option('--min-vulnerability-create-time')
@click.option('--max-vulnerability-create-time')
@click.option('--min-vulnerability-update-time')
@click.option('--max-vulnerability-update-time')
@click.option('--min-vulnerability-open-time')
@click.option('--max-vulnerability-open-time')
@click.option('--min-vulnerability-close-time')
@click.option('--max-vulnerability-close-time')
@click.option('--limit', type=int)
@click.pass_context
def get_location_specifiers_by_asset_name(
        ctx: click.Context,
        asset_ids: Optional[str],
        asset_names: Optional[str],
        asset_tags: Optional[str],
        host_ids: Optional[str],
        hostnames: Optional[str],
        ip_addresses: Optional[str],
        os_types: Optional[str],
        os_versions: Optional[str],
        alive: Optional[bool],
        vulnerability_ids: Optional[str],
        vulnerability_names: Optional[str],
        cve_ids: Optional[str],
        min_asset_create_time: Optional[str],
        max_asset_create_time: Optional[str],
        min_asset_update_time: Optional[str],
        max_asset_update_time: Optional[str],
        min_next_assessment_time: Optional[str],
        max_next_assessment_time: Optional[str],
        min_last_assessment_time: Optional[str],
        max_last_assessment_time: Optional[str],
        min_last_host_scan_time: Optional[str],
        max_last_host_scan_time: Optional[str],
        min_host_last_seen_time: Optional[str],
        max_host_last_seen_time: Optional[str],
        min_vulnerability_create_time: Optional[str],
        max_vulnerability_create_time: Optional[str],
        min_vulnerability_update_time: Optional[str],
        max_vulnerability_update_time: Optional[str],
        min_vulnerability_open_time: Optional[str],
        max_vulnerability_open_time: Optional[str],
        min_vulnerability_close_time: Optional[str],
        max_vulnerability_close_time: Optional[str],
        limit: Optional[int] = None):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    locations = {}
    for asset in api.iter_assets(
            ids=cli.str_to_ints(asset_ids),
            names=cli.str_to_strs(asset_names),
            tags=cli.str_to_strs(asset_tags),
            host_ids=cli.str_to_ints(host_ids),
            hostnames=cli.str_to_strs(hostnames),
            ip_addresses=cli.str_to_strs(ip_addresses),
            os_types=cli.str_to_strs(os_types),
            os_versions=cli.str_to_strs(os_versions),
            alive=alive,
            vulnerability_ids=cli.str_to_ints(vulnerability_ids),
            vulnerability_names=cli.str_to_strs(vulnerability_names),
            cve_ids=cli.str_to_strs(cve_ids),
            min_asset_create_time=cli.str_to_datetime(min_asset_create_time),
            max_asset_create_time=cli.str_to_datetime(max_asset_create_time),
            min_asset_update_time=cli.str_to_datetime(min_asset_update_time),
            max_asset_update_time=cli.str_to_datetime(max_asset_update_time),
            min_next_assessment_time=cli.str_to_datetime(min_next_assessment_time),
            max_next_assessment_time=cli.str_to_datetime(max_next_assessment_time),
            min_last_assessment_time=cli.str_to_datetime(min_last_assessment_time),
            max_last_assessment_time=cli.str_to_datetime(max_last_assessment_time),
            min_last_host_scan_time=cli.str_to_datetime(min_last_host_scan_time),
            max_last_host_scan_time=cli.str_to_datetime(max_last_host_scan_time),
            min_host_last_seen_time=cli.str_to_datetime(min_host_last_seen_time),
            max_host_last_seen_time=cli.str_to_datetime(max_host_last_seen_time),
            min_vulnerability_create_time=cli.str_to_datetime(min_vulnerability_create_time),
            max_vulnerability_create_time=cli.str_to_datetime(max_vulnerability_create_time),
            min_vulnerability_update_time=cli.str_to_datetime(min_vulnerability_update_time),
            max_vulnerability_update_time=cli.str_to_datetime(max_vulnerability_update_time),
            min_vulnerability_open_time=cli.str_to_datetime(min_vulnerability_open_time),
            max_vulnerability_open_time=cli.str_to_datetime(max_vulnerability_open_time),
            min_vulnerability_close_time=cli.str_to_datetime(min_vulnerability_close_time),
            max_vulnerability_close_time=cli.str_to_datetime(max_vulnerability_close_time),
            limit=limit,
    ):
        locations[asset.name] = [loc.to_dict() for loc in asset.location_specifiers]

    txt = json.dumps(locations, indent=DEFAULT_INDENT, sort_keys=SORT_KEYS_BY_DEFAULT)
    click.echo(txt)


@assets.command()
@click.option('--asset-ids')
@click.option('--asset-names')
@click.option('--asset-tags')
@click.option('--host-ids')
@click.option('--hostnames')
@click.option('--ip-addresses')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--alive/--dead', default=None)
@click.option('--vulnerability-ids')
@click.option('--vulnerability-names')
@click.option('--cve-ids')
@click.option('--min-asset-create-time')
@click.option('--max-asset-create-time')
@click.option('--min-asset-update-time')
@click.option('--max-asset-update-time')
@click.option('--min-next-assessment-time')
@click.option('--max-next-assessment-time')
@click.option('--min-last-assessment-time')
@click.option('--max-last-assessment-time')
@click.option('--min-last-host-scan-time')
@click.option('--max-last-host-scan-time')
@click.option('--min-host-last-seen-time')
@click.option('--max-host-last-seen-time')
@click.option('--min-vulnerability-create-time')
@click.option('--max-vulnerability-create-time')
@click.option('--min-vulnerability-update-time')
@click.option('--max-vulnerability-update-time')
@click.option('--min-vulnerability-open-time')
@click.option('--max-vulnerability-open-time')
@click.option('--min-vulnerability-close-time')
@click.option('--max-vulnerability-close-time')
@click.pass_context
def get_asset_tags(
        ctx: click.Context,
        asset_ids: Optional[str],
        asset_names: Optional[str],
        asset_tags: Optional[str],
        host_ids: Optional[str],
        hostnames: Optional[str],
        ip_addresses: Optional[str],
        os_types: Optional[str],
        os_versions: Optional[str],
        alive: Optional[bool],
        vulnerability_ids: Optional[str],
        vulnerability_names: Optional[str],
        cve_ids: Optional[str],
        min_asset_create_time: Optional[str],
        max_asset_create_time: Optional[str],
        min_asset_update_time: Optional[str],
        max_asset_update_time: Optional[str],
        min_next_assessment_time: Optional[str],
        max_next_assessment_time: Optional[str],
        min_last_assessment_time: Optional[str],
        max_last_assessment_time: Optional[str],
        min_last_host_scan_time: Optional[str],
        max_last_host_scan_time: Optional[str],
        min_host_last_seen_time: Optional[str],
        max_host_last_seen_time: Optional[str],
        min_vulnerability_create_time: Optional[str],
        max_vulnerability_create_time: Optional[str],
        min_vulnerability_update_time: Optional[str],
        max_vulnerability_update_time: Optional[str],
        min_vulnerability_open_time: Optional[str],
        max_vulnerability_open_time: Optional[str],
        min_vulnerability_close_time: Optional[str],
        max_vulnerability_close_time: Optional[str]):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    rows = api.iter_assets(
        ids=cli.str_to_ints(asset_ids),
        names=cli.str_to_strs(asset_names),
        tags=cli.str_to_strs(asset_tags),
        host_ids=cli.str_to_ints(host_ids),
        hostnames=cli.str_to_strs(hostnames),
        ip_addresses=cli.str_to_strs(ip_addresses),
        os_types=cli.str_to_strs(os_types),
        os_versions=cli.str_to_strs(os_versions),
        alive=alive,
        vulnerability_ids=cli.str_to_ints(vulnerability_ids),
        vulnerability_names=cli.str_to_strs(vulnerability_names),
        cve_ids=cli.str_to_strs(cve_ids),
        min_asset_create_time=cli.str_to_datetime(min_asset_create_time),
        max_asset_create_time=cli.str_to_datetime(max_asset_create_time),
        min_asset_update_time=cli.str_to_datetime(min_asset_update_time),
        max_asset_update_time=cli.str_to_datetime(max_asset_update_time),
        min_next_assessment_time=cli.str_to_datetime(min_next_assessment_time),
        max_next_assessment_time=cli.str_to_datetime(max_next_assessment_time),
        min_last_assessment_time=cli.str_to_datetime(min_last_assessment_time),
        max_last_assessment_time=cli.str_to_datetime(max_last_assessment_time),
        min_last_host_scan_time=cli.str_to_datetime(min_last_host_scan_time),
        max_last_host_scan_time=cli.str_to_datetime(max_last_host_scan_time),
        min_host_last_seen_time=cli.str_to_datetime(min_host_last_seen_time),
        max_host_last_seen_time=cli.str_to_datetime(max_host_last_seen_time),
        min_vulnerability_create_time=cli.str_to_datetime(min_vulnerability_create_time),
        max_vulnerability_create_time=cli.str_to_datetime(max_vulnerability_create_time),
        min_vulnerability_update_time=cli.str_to_datetime(min_vulnerability_update_time),
        max_vulnerability_update_time=cli.str_to_datetime(max_vulnerability_update_time),
        min_vulnerability_open_time=cli.str_to_datetime(min_vulnerability_open_time),
        max_vulnerability_open_time=cli.str_to_datetime(max_vulnerability_open_time),
        min_vulnerability_close_time=cli.str_to_datetime(min_vulnerability_close_time),
        max_vulnerability_close_time=cli.str_to_datetime(max_vulnerability_close_time),
    )
    tags = sorted(set(itertools.chain.from_iterable(row.tags for row in rows)))
    click.echo(json.dumps(tags))


@assets.command()
@click.option('--asset-ids')
@click.option('--asset-names')
@click.option('--asset-tags')
@click.option('--host-ids')
@click.option('--hostnames')
@click.option('--ip-addresses')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--alive/--dead', default=None)
@click.option('--vulnerability-ids')
@click.option('--vulnerability-names')
@click.option('--cve-ids')
@click.option('--min-asset-create-time')
@click.option('--max-asset-create-time')
@click.option('--min-asset-update-time')
@click.option('--max-asset-update-time')
@click.option('--min-next-assessment-time')
@click.option('--max-next-assessment-time')
@click.option('--min-last-assessment-time')
@click.option('--max-last-assessment-time')
@click.option('--min-last-host-scan-time')
@click.option('--max-last-host-scan-time')
@click.option('--min-host-last-seen-time')
@click.option('--max-host-last-seen-time')
@click.option('--min-vulnerability-create-time')
@click.option('--max-vulnerability-create-time')
@click.option('--min-vulnerability-update-time')
@click.option('--max-vulnerability-update-time')
@click.option('--min-vulnerability-open-time')
@click.option('--max-vulnerability-open-time')
@click.option('--min-vulnerability-close-time')
@click.option('--max-vulnerability-close-time')
@click.pass_context
def get_asset_names(
        ctx: click.Context,
        asset_ids: Optional[str],
        asset_names: Optional[str],
        asset_tags: Optional[str],
        host_ids: Optional[str],
        hostnames: Optional[str],
        ip_addresses: Optional[str],
        os_types: Optional[str],
        os_versions: Optional[str],
        alive: Optional[bool],
        vulnerability_ids: Optional[str],
        vulnerability_names: Optional[str],
        cve_ids: Optional[str],
        min_asset_create_time: Optional[str],
        max_asset_create_time: Optional[str],
        min_asset_update_time: Optional[str],
        max_asset_update_time: Optional[str],
        min_next_assessment_time: Optional[str],
        max_next_assessment_time: Optional[str],
        min_last_assessment_time: Optional[str],
        max_last_assessment_time: Optional[str],
        min_last_host_scan_time: Optional[str],
        max_last_host_scan_time: Optional[str],
        min_host_last_seen_time: Optional[str],
        max_host_last_seen_time: Optional[str],
        min_vulnerability_create_time: Optional[str],
        max_vulnerability_create_time: Optional[str],
        min_vulnerability_update_time: Optional[str],
        max_vulnerability_update_time: Optional[str],
        min_vulnerability_open_time: Optional[str],
        max_vulnerability_open_time: Optional[str],
        min_vulnerability_close_time: Optional[str],
        max_vulnerability_close_time: Optional[str]):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    rows = api.iter_assets(
        ids=cli.str_to_ints(asset_ids),
        names=cli.str_to_strs(asset_names),
        tags=cli.str_to_strs(asset_tags),
        host_ids=cli.str_to_ints(host_ids),
        hostnames=cli.str_to_strs(hostnames),
        ip_addresses=cli.str_to_strs(ip_addresses),
        os_types=cli.str_to_strs(os_types),
        os_versions=cli.str_to_strs(os_versions),
        alive=alive,
        vulnerability_ids=cli.str_to_ints(vulnerability_ids),
        vulnerability_names=cli.str_to_strs(vulnerability_names),
        cve_ids=cli.str_to_strs(cve_ids),
        min_asset_create_time=cli.str_to_datetime(min_asset_create_time),
        max_asset_create_time=cli.str_to_datetime(max_asset_create_time),
        min_asset_update_time=cli.str_to_datetime(min_asset_update_time),
        max_asset_update_time=cli.str_to_datetime(max_asset_update_time),
        min_next_assessment_time=cli.str_to_datetime(min_next_assessment_time),
        max_next_assessment_time=cli.str_to_datetime(max_next_assessment_time),
        min_last_assessment_time=cli.str_to_datetime(min_last_assessment_time),
        max_last_assessment_time=cli.str_to_datetime(max_last_assessment_time),
        min_last_host_scan_time=cli.str_to_datetime(min_last_host_scan_time),
        max_last_host_scan_time=cli.str_to_datetime(max_last_host_scan_time),
        min_host_last_seen_time=cli.str_to_datetime(min_host_last_seen_time),
        max_host_last_seen_time=cli.str_to_datetime(max_host_last_seen_time),
        min_vulnerability_create_time=cli.str_to_datetime(min_vulnerability_create_time),
        max_vulnerability_create_time=cli.str_to_datetime(max_vulnerability_create_time),
        min_vulnerability_update_time=cli.str_to_datetime(min_vulnerability_update_time),
        max_vulnerability_update_time=cli.str_to_datetime(max_vulnerability_update_time),
        min_vulnerability_open_time=cli.str_to_datetime(min_vulnerability_open_time),
        max_vulnerability_open_time=cli.str_to_datetime(max_vulnerability_open_time),
        min_vulnerability_close_time=cli.str_to_datetime(min_vulnerability_close_time),
        max_vulnerability_close_time=cli.str_to_datetime(max_vulnerability_close_time),
    )
    seen = sorted([asset.name for asset in rows])
    click.echo(json.dumps(seen, indent=DEFAULT_INDENT, sort_keys=SORT_KEYS_BY_DEFAULT))


@assets.command()
@click.option('--asset-ids')
@click.option('--asset-names')
@click.option('--asset-tags')
@click.option('--host-ids')
@click.option('--hostnames')
@click.option('--ip-addresses')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--alive/--dead', default=None)
@click.option('--vulnerability-ids')
@click.option('--vulnerability-names')
@click.option('--cve-ids')
@click.option('--min-asset-create-time')
@click.option('--max-asset-create-time')
@click.option('--min-asset-update-time')
@click.option('--max-asset-update-time')
@click.option('--min-next-assessment-time')
@click.option('--max-next-assessment-time')
@click.option('--min-last-assessment-time')
@click.option('--max-last-assessment-time')
@click.option('--min-last-host-scan-time')
@click.option('--max-last-host-scan-time')
@click.option('--min-host-last-seen-time')
@click.option('--max-host-last-seen-time')
@click.option('--min-vulnerability-create-time')
@click.option('--max-vulnerability-create-time')
@click.option('--min-vulnerability-update-time')
@click.option('--max-vulnerability-update-time')
@click.option('--min-vulnerability-open-time')
@click.option('--max-vulnerability-open-time')
@click.option('--min-vulnerability-close-time')
@click.option('--max-vulnerability-close-time')
@click.pass_context
def count_assets(
        ctx: click.Context,
        asset_ids: Optional[str],
        asset_names: Optional[str],
        asset_tags: Optional[str],
        host_ids: Optional[str],
        hostnames: Optional[str],
        ip_addresses: Optional[str],
        os_types: Optional[str],
        os_versions: Optional[str],
        alive: Optional[bool],
        vulnerability_ids: Optional[str],
        vulnerability_names: Optional[str],
        cve_ids: Optional[str],
        min_asset_create_time: Optional[str],
        max_asset_create_time: Optional[str],
        min_asset_update_time: Optional[str],
        max_asset_update_time: Optional[str],
        min_next_assessment_time: Optional[str],
        max_next_assessment_time: Optional[str],
        min_last_assessment_time: Optional[str],
        max_last_assessment_time: Optional[str],
        min_last_host_scan_time: Optional[str],
        max_last_host_scan_time: Optional[str],
        min_host_last_seen_time: Optional[str],
        max_host_last_seen_time: Optional[str],
        min_vulnerability_create_time: Optional[str],
        max_vulnerability_create_time: Optional[str],
        min_vulnerability_update_time: Optional[str],
        max_vulnerability_update_time: Optional[str],
        min_vulnerability_open_time: Optional[str],
        max_vulnerability_open_time: Optional[str],
        min_vulnerability_close_time: Optional[str],
        max_vulnerability_close_time: Optional[str]):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    total = api.count_assets(
        ids=cli.str_to_ints(asset_ids),
        names=cli.str_to_strs(asset_names),
        tags=cli.str_to_strs(asset_tags),
        host_ids=cli.str_to_ints(host_ids),
        hostnames=cli.str_to_strs(hostnames),
        ip_addresses=cli.str_to_strs(ip_addresses),
        os_types=cli.str_to_strs(os_types),
        os_versions=cli.str_to_strs(os_versions),
        alive=alive,
        vulnerability_ids=cli.str_to_ints(vulnerability_ids),
        vulnerability_names=cli.str_to_strs(vulnerability_names),
        cve_ids=cli.str_to_strs(cve_ids),
        min_asset_create_time=cli.str_to_datetime(min_asset_create_time),
        max_asset_create_time=cli.str_to_datetime(max_asset_create_time),
        min_asset_update_time=cli.str_to_datetime(min_asset_update_time),
        max_asset_update_time=cli.str_to_datetime(max_asset_update_time),
        min_next_assessment_time=cli.str_to_datetime(min_next_assessment_time),
        max_next_assessment_time=cli.str_to_datetime(max_next_assessment_time),
        min_last_assessment_time=cli.str_to_datetime(min_last_assessment_time),
        max_last_assessment_time=cli.str_to_datetime(max_last_assessment_time),
        min_last_host_scan_time=cli.str_to_datetime(min_last_host_scan_time),
        max_last_host_scan_time=cli.str_to_datetime(max_last_host_scan_time),
        min_host_last_seen_time=cli.str_to_datetime(min_host_last_seen_time),
        max_host_last_seen_time=cli.str_to_datetime(max_host_last_seen_time),
        min_vulnerability_create_time=cli.str_to_datetime(min_vulnerability_create_time),
        max_vulnerability_create_time=cli.str_to_datetime(max_vulnerability_create_time),
        min_vulnerability_update_time=cli.str_to_datetime(min_vulnerability_update_time),
        max_vulnerability_update_time=cli.str_to_datetime(max_vulnerability_update_time),
        min_vulnerability_open_time=cli.str_to_datetime(min_vulnerability_open_time),
        max_vulnerability_open_time=cli.str_to_datetime(max_vulnerability_open_time),
        min_vulnerability_close_time=cli.str_to_datetime(min_vulnerability_close_time),
        max_vulnerability_close_time=cli.str_to_datetime(max_vulnerability_close_time)
    )
    click.echo(total)
