from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from celery.task.schedules import crontab
from django.utils import timezone
from .models import Order

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_check_expired_order",
    ignore_result=True
)
def task_check_expired_order():
    orders = Order.objects.filter(status=100)
    for order in orders:
        if (order.created_on + timezone.timedelta(seconds=60)) <= timezone.now():
            order.status = 500
            order.save()
            logger.info('Order expired! Number: {0}, Customer: {1}, Cost: {2}.'.format(order.number, order.customer,
                                                                                       order.cost))


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_update_report",
    ignore_result=True
)
def task_update_report():
    orders = Order.objects.filter(created_on__gte=timezone.now() - timezone.timedelta(seconds=60))
    if orders:
        info = ''
        for order in orders:
            info += 'New order! Created: {0}, Number: {1}, Customer: {2}, Cost: {3}.\n'.format(order.created_on,
                                                                                               order.number,
                                                                                               order.customer,
                                                                                               order.cost)
        with open('celery_report.txt', 'a+') as f:
            f.write(info)
        logger.info(
            'New order added to report.txt! Number: {0}, Customer: {1}, Cost: {2}.\n'.format(order.number,
                                                                                             order.customer,
                                                                                             order.cost))
