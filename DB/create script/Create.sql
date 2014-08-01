CREATE TABLE  PostsTesting (
    Id   VARCHAR(50) PRIMARY KEY,
    PostTypeId    VARCHAR(50),
    ParentID VARCHAR(20),
    AcceptedAnswerId VARCHAR(20),
    CreationDate TIMESTAMPTZ,
    Score INTEGER,
    ViewCount INTEGER,
    Body VARCHAR(55000),
    OwnerUserId VARCHAR(30),
    LastEditorUserId VARCHAR(30),
    LastEditorDisplayName VARCHAR(150),
    LastEditDate TIMESTAMPTZ,
    LastActivityDate TIMESTAMPTZ,
    CommunityOwnedDate TIMESTAMPTZ,
    ClosedDate TIMESTAMPTZ,
    Title VARCHAR(400),
    Tags VARCHAR(150),
    AnswerCount INTEGER,
    CommentCount INTEGER,
    FavoriteCount INTEGER
);
CREATE TABLE  TagSynonyms (
    id   VARCHAR(50) PRIMARY KEY,
    applied_count INTEGER,
    from_tag    VARCHAR(50),
    to_tag    VARCHAR(50)
);