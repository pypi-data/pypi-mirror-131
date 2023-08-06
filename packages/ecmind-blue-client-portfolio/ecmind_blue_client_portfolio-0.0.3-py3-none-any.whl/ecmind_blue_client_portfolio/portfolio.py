from typing import List, Optional, Union
from ecmind_blue_client import Client, Job, Param, ParamTypes
from XmlElement import XmlElement
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class PortfolioObject:
    """Class to store portfolio member objects."""
    id: int
    type_id: int


@dataclass(frozen=True)
class Portfolio:
    """Class to store a portfolio."""
    id: int
    created: datetime
    creator: str
    recipient: str
    subject: str
    type_id: Union[None, int]
    objects: List[PortfolioObject]


def search(client: Client, id: int = None, creator: str = None, recipient: str = None, 
    subject: str = None, created: datetime = None, created_max_date: datetime = None, 
    garbage_mode: bool = False, type_id: Union[None, int] = None
    ) -> List[Portfolio]:
    """Search for portfolios.

        Keyword arguments:
        client -- A instance of ecmind_blue_client.Client().
        id -- (Optional) The portfolio id to search for. 
        creator -- (Optional) Username of the portfolio creator to search for. 
        recipient -- (Optional) Username of the portfolio recipient to search for. 
        subject -- (Optional) Subject of the portfolio to search for. 
        garbage_mode -- (Optional) bool indicating, if the query searches the recycle bin instead of non-deleted portfolios, default = False.
        type_id -- (Optional) object type if for typed portfolios.
    """

    portfolio_xml = XmlElement.from_object('Portfolio', {
        '@creator': creator or '',
        '@recipient': recipient or '',
        '@subject': subject or '',
    })

    if created:
        portfolio_xml.set('created', created.strftime('%s'))

    if id != None:
        portfolio_xml.set('id', str(id))

    if type_id != None:
        portfolio_xml.set('objtype', str(type_id))

    job = Job(
        'dms.RetrievePortfolios',
        Flags=0,
        GarbageMode=1 if garbage_mode else 0,
        Created_to=int(created_max_date.strftime('%s')
                       ) if created_max_date else 0
    )

    job.append(Param('PortfolioXML', ParamTypes.BASE64,
               portfolio_xml.to_string()))

    result = client.execute(job)

    if result.return_code != 0:
        raise RuntimeError(result.error_message)

    result_xml = XmlElement.from_string(result.values['PortfoliosXML'])

    if not result_xml.find('Portfolio'):
        return []

    for elem in result_xml.walk():
        if elem.name in ['Portfolio', 'Object']:
            elem.flag_as_list = True

    result = []
    for portfolio in result_xml.to_dict(recognize_bool=False)['Portfolio']:
        result.append(Portfolio(
            id=portfolio['@id'],
            created=datetime.fromtimestamp(portfolio['@created']),
            creator=portfolio['@creator'],
            recipient=portfolio['@recipient'],
            subject=portfolio['@subject'],
            type_id=(int(portfolio['@objtype']) if '@objtype' in portfolio and int(portfolio['@objtype']) > 0 else None),
            objects=[PortfolioObject(id=obj['@id'], type_id=obj['@objecttype_id']) for obj in portfolio['Objects']
                     ['Object']] if (portfolio['Objects'] and 'Object' in portfolio['Objects']) else []
        ))

    return result


def user_favorites(client: Client, username: str) -> Union[Portfolio, None]:
    """Shortcut function to search for a users favorites portfolio."""

    p = search(client, creator=username, recipient=username,
               created=datetime(1970, 1, 1, 1, 0, 3))
    if len(p) == 1:
        return p[0]
    else:
        return None


def create(client: Client, creator: str = None, recipient: str = None, 
    subject: str = None, objects: Optional[List[PortfolioObject]] = None,
    type_id: Union[None, int] = None) -> int:
    """Create a portfolio and return its id.

        Keyword arguments:
        client -- A instance of ecmind_blue_client.Client().
        creator -- (Optional) Username of the portfolio creator to search for. 
        recipient -- (Optional) Username of the portfolio recipient to search for. 
        subject -- (Optional) Subject of the portfolio to search for. 
        objects -- (Optional) List of `PortfolioObject`s.
        type_id -- (Optional) object type if for typed portfolios.
    """
    if objects:
        portfolio_objects = {'Object': [
            {'@id': obj.id, '@objecttype_id': obj.type_id}
            for obj in objects
        ]}
    else:
        portfolio_objects = []

    portfolio_xml = XmlElement.from_object('Portfolio', {
        '@creator': creator or '',
        '@recipient': recipient or '',
        '@subject': subject or '',
        'Objects': portfolio_objects
    })

    if type_id != None:
        portfolio_xml.set('objtype', str(type_id))

    job = Job(
        jobname='dms.AddPortfolio',
        Flags=0,
        Mode=1
    )

    job.append(Param('PortfolioXML', ParamTypes.BASE64,
               portfolio_xml.to_string()))

    result = client.execute(job)
    if result.return_code != 0:
        raise RuntimeError(result.error_message)

    return result.values['PortfolioID']


def delete(client: Client, portfolio_or_id: Union[Portfolio, int]) -> None:
    '''Delete a portfolio by its id.'''
    if isinstance(portfolio_or_id, Portfolio):
        id = portfolio_or_id.id
    else:
        id = int(portfolio_or_id)

    portfolio_xml = XmlElement.from_object('Portfolio', {
        '@id': id
    })

    job = Job(jobname='dms.DelPortfolio', Flags=0)
    job.append(Param('PortfolioXML', ParamTypes.BASE64,
               portfolio_xml.to_string()))

    result = client.execute(job)
    if result.return_code != 0:
        raise RuntimeError(result.error_message)

    return None


def delete_for(client: Client, recipient: str, subject: str) -> None:
    '''Delete a portfolio by its recipient and subject.'''

    portfolio_xml = XmlElement.from_object('Portfolio', {
        '@recipient': recipient,
        '@subject': subject,
    })

    job = Job(jobname='dms.DelPortfolio', Flags=0)
    job.append(Param('PortfolioXML', ParamTypes.BASE64,
               portfolio_xml.to_string()))

    result = client.execute(job)
    if result.return_code != 0:
        raise RuntimeError(result.error_message)

    return None


def remove_objects(client: Client, portfolio_or_id: Union[Portfolio, int], objects: List[PortfolioObject]):
    '''Remove objects from a portfolio.'''

    if isinstance(portfolio_or_id, Portfolio):
        id = portfolio_or_id.id
    else:
        id = int(portfolio_or_id)

    portfolio_xml = XmlElement.from_object('Portfolio', {
        '@id': id,
        'Objects': {'Object': [
            {'@id': obj.id, '@objecttype_id': obj.type_id}
            for obj in objects
        ]}
    })

    job = Job(jobname='dms.RemoveFromportfolio', Flags=0)
    job.append(Param('PortfolioXML', ParamTypes.BASE64,
               portfolio_xml.to_string()))

    result = client.execute(job)
    if result.return_code != 0:
        raise RuntimeError(result.error_message)

    return None


def add_objects(client: Client, portfolio_or_id: Union[Portfolio, int], objects: List[PortfolioObject], replace_existing_object_list: bool = False):
    '''Add new objects to a portfolio. Set `replace_existing_object_list` to clear portfolio upfront.'''

    if isinstance(portfolio_or_id, Portfolio):
        id = portfolio_or_id.id
    else:
        id = int(portfolio_or_id)

    portfolio_xml = XmlElement.from_object('Portfolio', {
        '@id': id,
        'Objects': {'Object': [
            {'@id': obj.id, '@objecttype_id': obj.type_id}
            for obj in objects
        ]}
    })

    job = Job(
        jobname='dms.ModPortfolio',
        Flags=0,
        Mode=(1 if replace_existing_object_list else 0)
    )
    job.append(Param('PortfolioXML', ParamTypes.BASE64,
               portfolio_xml.to_string()))

    result = client.execute(job)
    if result.return_code != 0:
        raise RuntimeError(result.error_message)

    return None


def clear_objects(client: Client, portfolio_or_id: Union[Portfolio, int]):
    '''Shortcut function to remove all objects from a portfolio.'''

    return add_objects(client, portfolio_or_id, [], True)
