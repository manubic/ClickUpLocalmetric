from lib.google.GoogleSheets import Sheets
from lib.db.sql import SQL
from credentials.config import Config
from datetime import datetime, timedelta
import json



class Localmetric:
    def __init__(self, config: Config, creds):
        self.__SQL = SQL(config.DBUser, config.DBHost, config.DBName, config.DBPassword)
        self.__EmailsSheet = Sheets(config.EmailsSheetID, creds)
        self.__allRowsEmailsSheet = self.__EmailsSheet.getAllRows('Clientes')[1:]
        self.__AccountsInfo = self.__getAccountsID(complete=True)
    
    def __getAccountsID(self, complete: bool = False) -> list[str]:
        return [
            row[5].replace('_', '/')
            for row in self.__allRowsEmailsSheet
        ] if not complete else {
            row[5].replace('_', '/'): self.__SQL.query(f'SELECT name FROM accounts WHERE id = "{row[5].replace('_', '/')}"')[0][0]
            for row in self.__allRowsEmailsSheet
        }
    
    def getClientsLocations(self) -> dict[str, str]:
        _clientsLocations: dict[str, str] = {}
        for row in self.__allRowsEmailsSheet:
            clientName = self.__AccountsInfo[row[5].replace('_', '/')]
            for locationName in self.__SQL.query(f'SELECT location_name FROM locations WHERE account_id = "{row[5].replace('_', '/')}"'):
                _clientsLocations[locationName[0]] = clientName
        return _clientsLocations

    def getClientsEmails(self) -> dict[str, str]:
        _clientsEmails = {}
        for sheet in self.__EmailsSheet.getSheets():
            for row in self.__EmailsSheet.getAllRows(sheet):
                _clientsEmails[row[2].split(' - ')[0].replace('_', '/')] = row[1]
        return _clientsEmails
    
    def getClientsOwners(self) -> dict[str, list[str]]:
        _owners = {}
        for row in self.__allRowsEmailsSheet:
            if len(row) > 5:
                _owners[row[8]] = _owners.get(row[8], []) + [self.__AccountsInfo[row[5].replace('_', '/')]]
        return _owners
    
    def getNegativeReviewsFromOneMonth(self) -> list[list[str | datetime | int]]:
        return [
            [
                review[0], review[1], json.loads(review[2])['displayName'], 
                'Sin comentario' if review[3] == None else review[3].split('(Original)\n')[-1], review[4],
                review[5], json.loads(review[6])['addressLines'][0], review[7], review[8]
            ]
            for review in self.__SQL.query(f"""
                    SELECT r.create_time, l.location_name, r.reviewer, r.comment, r.star_rating, r.id, l.address, l.id, l.account_id
                    FROM reviews AS r
                    INNER JOIN (SELECT id, location_name, account_id, address
                        FROM locations
                        WHERE account_id IN ('{"', '".join(self.__getAccountsID()).replace(' ', '')}')
                    ) AS l ON r.location_id = l.id
                    WHERE
                        r.review_reply IS NULL 
                        AND r.star_rating <= 3 
                        AND r.create_time >= '{(datetime.now() - timedelta(days=30)).replace(hour=0, minute=0, second=1)}'
                    ORDER BY 
                        r.create_time ASC;
                """)
            ]