__author__ = 'Dmitry Golubkov'

import re
import cx_Oracle
from .log import Logger

logger = Logger().get()


# noinspection PyBroadException
def get_dataset_popularity_by_tasks(connection_string,
                                    from_date,
                                    to_date,
                                    ignore_tid=True,
                                    max_length=None,
                                    min_value=None):
    """
    Calculates popularity (by number of tasks) of each input dataset used during the specified period,
    resulted dataset list is sorted by popularity value (from max to min)

    :param connection_string: Oracle database connection string to access ATLAS_PANDA.* tables
    :param from_date: start date of specified period
    :param to_date: end date of specified period
    :param ignore_tid: combine the popularity of datasets with same container,
    ignoring _tidXXXXXXXX_00 at the end of dataset name
    :param max_length: print only first max_length datasets
    :param min_value: do not print datasets with popularity value less than min_value
    :return: dataset popularity dict or None in case of error
    """
    try:
        logger.info('calculates popularity using tasks from {0} to {1}'.format(
            from_date.strftime('%d-%m-%Y'), to_date.strftime('%d-%m-%Y'))
        )
        dataset_pattern = re.compile(r'^(mc.*|data).*\.DAOD.*\..*$')
        tid_pattern = re.compile(r'_tid\d+_00')
        connection = cx_Oracle.connect(connection_string)
        cursor = connection.cursor()
        query = \
            "SELECT jeditaskid, taskname, status, username, starttime, endtime, campaign, site " + \
            "FROM ATLAS_PANDA.JEDI_TASKS WHERE status in ('done', 'finished') AND prodsourcelabel='user' " + \
            "AND starttime >= TO_DATE('{0}', 'DD-MM-YYYY') ".format(from_date.strftime('%d-%m-%Y')) + \
            "AND starttime < TO_DATE('{0}', 'DD-MM-YYYY') + 1 ".format(to_date.strftime('%d-%m-%Y')) + \
            "ORDER BY jeditaskid ASC"
        tasks = [task[0] for task in cursor.execute(query)]
        datasets = dict()
        for task_id in tasks:
            query = \
                "SELECT datasetname FROM ATLAS_PANDA.JEDI_DATASETS WHERE jeditaskid={0} AND type='input'".format(
                    task_id)
            result = cursor.execute(query)
            for dataset in result:
                name = dataset[0].split(':')[-1]
                if ignore_tid:
                    name = re.sub(tid_pattern, '', name)
                if not dataset_pattern.match(name):
                    continue
                if name not in datasets.keys():
                    datasets[name] = 0
                datasets[name] += 1
        datasets_sorted = \
            {key: value for key, value in sorted(datasets.items(), key=lambda item: item[1], reverse=True)}
        length = len(datasets_sorted)
        for key, value in list(datasets_sorted.items())[:max_length or length]:
            if min_value is not None:
                if value < min_value:
                    continue
            logger.info('{0}: {1}'.format(key, value))
        return datasets_sorted
    except Exception as ex:
        logger.exception('exception occurred: {0}'.format(ex))
        return None
