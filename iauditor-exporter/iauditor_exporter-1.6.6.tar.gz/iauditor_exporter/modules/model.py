from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime,
    Boolean,
    BigInteger,
    Unicode,
    schema,
)


def set_table(table, merge, Base, user_schema=None):
    class Database(Base):
        __tablename__ = table
        if user_schema:
            __table_args__ = {"schema": user_schema}
        SortingIndex = Column(Integer)
        ItemType = Column(String(20))
        Label = Column(Unicode())
        Response = Column(Unicode())
        Comment = Column(Unicode())
        MediaHypertextReference = Column(Unicode())
        Latitude = Column(String(50))
        Longitude = Column(String(50))
        ItemScore = Column(Float)
        ItemMaxScore = Column(Float)
        ItemScorePercentage = Column(Float)
        Mandatory = Column(Boolean)
        FailedResponse = Column(Boolean)
        Inactive = Column(Boolean)
        AuditID = Column(String(100), primary_key=True, autoincrement=False)
        ItemID = Column(String(100), primary_key=True, autoincrement=False)
        if merge is False:
            DatePK = Column(BigInteger, primary_key=True, autoincrement=False)
        else:
            DatePK = Column(BigInteger)
        ResponseID = Column(Unicode())
        ParentID = Column(String(100))
        AuditOwner = Column(Unicode())
        AuditAuthor = Column(Unicode())
        AuditOwnerID = Column(Unicode())
        AuditAuthorID = Column(String(100))
        AuditName = Column(Unicode())
        AuditScore = Column(Float)
        AuditMaxScore = Column(Float)
        AuditScorePercentage = Column(Float)
        AuditDuration = Column(Float)
        DateStarted = Column(DateTime)
        DateCompleted = Column(DateTime)
        DateModified = Column(DateTime)
        TemplateID = Column(String(100))
        TemplateName = Column(Unicode())
        TemplateAuthor = Column(Unicode())
        TemplateAuthorID = Column(String(100))
        ItemCategory = Column(Unicode())
        RepeatingSectionParentID = Column(String(100))
        DocumentNo = Column(Unicode())
        ConductedOn = Column(DateTime)
        PreparedBy = Column(Unicode())
        Location = Column(Unicode())
        Personnel = Column(Unicode())
        ClientSite = Column(Unicode())
        AuditSite = Column(Unicode())
        AuditArea = Column(Unicode())
        AuditRegion = Column(Unicode())
        Archived = Column(Boolean)
        if user_schema:
            schema = user_schema

    return Database


SQL_HEADER_ROW = [
    "SortingIndex",
    "ItemType",
    "Label",
    "Response",
    "Comment",
    "MediaHypertextReference",
    "Latitude",
    "Longitude",
    "ItemScore",
    "ItemMaxScore",
    "ItemScorePercentage",
    "Mandatory",
    "FailedResponse",
    "Inactive",
    "ItemID",
    "ResponseID",
    "ParentID",
    "AuditOwner",
    "AuditAuthor",
    "AuditOwnerID",
    "AuditAuthorID",
    "AuditName",
    "AuditScore",
    "AuditMaxScore",
    "AuditScorePercentage",
    "AuditDuration",
    "DateStarted",
    "DateCompleted",
    "DateModified",
    "AuditID",
    "TemplateID",
    "TemplateName",
    "TemplateAuthor",
    "TemplateAuthorID",
    "ItemCategory",
    "RepeatingSectionParentID",
    "DocumentNo",
    "ConductedOn",
    "PreparedBy",
    "Location",
    "Personnel",
    "ClientSite",
    "AuditSite",
    "AuditArea",
    "AuditRegion",
    "Archived",
]


def set_actions_table(table, merge, Base, user_schema=None):
    class ActionsDatabase(Base):
        __tablename__ = table
        if user_schema:
            __table_args__ = {"schema": user_schema}
        id = Column(Integer, primary_key=False, autoincrement=True)
        title = Column(Unicode())
        description = Column(Unicode())
        assignee = Column(Unicode())
        priority = Column(Unicode())
        priorityCode = Column(Integer)
        status = Column(String(20))
        statusCode = Column(Integer)
        dueDatetime = Column(DateTime)
        actionId = Column(String(100), primary_key=True, autoincrement=False)
        if merge is False:
            DatePK = Column(BigInteger, autoincrement=False)
        else:
            DatePK = Column(BigInteger, primary_key=True, autoincrement=False)
        audit = Column(Unicode())
        auditId = Column(String(50))
        linkedToItem = Column(Unicode())
        linkedToItemId = Column(Unicode())
        creatorName = Column(Unicode())
        creatorId = Column(String(50))
        createdDatetime = Column(DateTime)
        modifiedDatetime = Column(DateTime)
        completedDatetime = Column(DateTime)
        if schema:
            schema = user_schema

    return ActionsDatabase


ACTIONS_HEADER_ROW = [
    "actionId",
    "title",
    "description",
    "assignee",
    "priority",
    "priorityCode",
    "status",
    "statusCode",
    "dueDatetime",
    "audit",
    "auditId",
    "linkedToItem",
    "linkedToItemId",
    "creatorName",
    "creatorId",
    "createdDatetime",
    "modifiedDatetime",
    "completedDatetime",
]
