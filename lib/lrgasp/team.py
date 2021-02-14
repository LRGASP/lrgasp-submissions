"""
Team metadata parsing and validation.
"""
import json
from lrgasp import LrgaspException, gopen
from lrgasp.objDict import ObjDict
from lrgasp.metadata_validate import Field, check_from_defs, validate_email, validate_http_url
from lrgasp.types import validate_symbolic_ident

##
# top-level team struct (from JSON)
##
fld_team_id = Field("team_id", validator=validate_symbolic_ident)
fld_group_name = Field("group_name")
fld_group_url = Field("group_url", optional=True, validator=validate_http_url)
fld_notes = Field("notes", allow_empty=True, optional=True)
fld_contacts = Field("contacts", list)

team_fields = (
    fld_team_id,
    fld_group_name,
    fld_group_url,
    fld_notes,
    fld_contacts
)

##
# contacts entries
##
fld_contact_name = Field("name", str)
fld_contact_email = Field("email", str, validator=validate_email)

team_contact_fields = (
    fld_contact_name,
    fld_contact_email,
    fld_notes
)

def team_contact_validate(contact):
    desc = "team.contacts"
    check_from_defs(desc, team_contact_fields, contact)

def team_validate(team):
    desc = "team"
    check_from_defs(desc, team_fields, team)
    try:
        validate_symbolic_ident(team.team_id)
    except LrgaspException as ex:
        raise LrgaspException(f"invalid {desc}.{fld_team_id.name}") from ex
    for contact in team.contacts:
        team_contact_validate(contact)

def team_load(team_json):
    """load and validate team metadata"""
    try:
        with gopen(team_json) as fh:
            team = json.load(fh, object_pairs_hook=ObjDict)
    except json.decoder.JSONDecodeError as ex:
        raise LrgaspException(f"parse of team metadata (JSON) failed: {team_json}") from ex
    try:
        team_validate(team)
    except LrgaspException as ex:
        raise LrgaspException(f"validation of team metadata failed: {team_json}") from ex
    return team
