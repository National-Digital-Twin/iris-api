from telicent_labels import SecurityLabelBuilder, TelicentSecurityLabelsV2
from enum import Enum
from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Dict

ies = "http://ies.data.gov.uk/ontology/ies4#"


class ClassificationEmum(str, Enum):
    official = "O"
    official_sensitive = "OS"
    secret = "S"
    top_secret = "TS"


class EDH(BaseModel):
    permitted_organisations: List[str] = []
    permitted_nationalities: List[str] = []
    classification: ClassificationEmum = "O"

    def to_string(self):
        builder = SecurityLabelBuilder()
        if len(self.permitted_organisations) > 0:
            builder.add_multiple(
                TelicentSecurityLabelsV2.PERMITTED_ORGANISATIONS.value,
                *self.permitted_organisations,
            )
        if len(self.permitted_nationalities) > 0:
            builder.add_multiple(
                TelicentSecurityLabelsV2.PERMITTED_NATIONALITIES.value,
                *self.permitted_nationalities,
            )
        if self.classification:
            builder.add(
                TelicentSecurityLabelsV2.CLASSIFICATION.value, self.classification.value
            )
        return builder.build()


class IesThing(BaseModel):
    """
    The top of the class tree
        uri - the uri of the created data object
    """

    uri: str = None
    securityLabel: EDH = None
    types: List[str] = []


class IesElement(IesThing):
    inPeriod: date = None
    pass


class IesEntity(IesElement):
    pass


class IesAssessment(IesThing):
    """
    An IES assessment - not used at this stage - please use IesAssessToBeTrue
    """

    assessedItem: str
    assessor: str
    assessmentType: str = None


class IesAssessToBeTrue(IesAssessment):
    """
    An assessment used to validate a statement or state
    """

    types: List[str] = [ies + "AssessToBeTrue"]


class IesAssessToBeFalse(IesAssessment):
    """
    An IES assessment used to invalidate a statement or state
    """

    types: List[str] = [ies + "AssessToBeFalse"]


class IesClass(IesThing):
    """
    An IES class (types of things) from the IES ontology, or from local extensions such as the NDT ontology extensions
    """

    shortName: str
    superClasses: List[str] = []
    description: List[str] = []


class IesState(IesElement):
    """
    A temporal stage of an element in IES - we use this here to identify the validity period of a building for the assessment being made
    """

    stateOf: str
    startDateTime: datetime = None
    endDateTime: datetime = None


class IesAccount(IesThing):
    """
    Not used at this stage
    """

    id: str
    name: str = None
    email: str = None


class IesPerson(IesThing):
    """
    A person - in this case of this API, this is the person who conducted the assessment
    """

    surname: str
    givenName: str


class Building(IesThing):
    uprn: str = None
    currentEnergyRating: str = None
    types: List[str] = []
    parentBuildingTOID: str = None
    buildingTOID: str = None
    parentBuilding: str = None
    flags: Dict = {}


class IesEntityAndStates(BaseModel):
    entity: IesEntity
    states: List[IesState]


class AccessUser(BaseModel):
    username: str
    user_id: str
    active: bool = None
    email: str = None
    attributes: dict[str, str]
    groups: List[str]
