procedures = {}

procedures['SIC_MAIL_CLIENTE_AT'] = '''
    CREATE OR ALTER PROCEDURE SIC_MAIL_CLIENTE_AT
    as
    BEGIN
        if (not exists(
        select 1 from RDB$RELATION_FIELDS rf
        where rf.RDB$RELATION_NAME = 'CLIENTES' and rf.RDB$FIELD_NAME = 'SIC_MAIL_NOENVIAR')) then
            execute statement 'ALTER TABLE CLIENTES ADD SIC_MAIL_NOENVIAR SMALLINT';
    END
    '''
