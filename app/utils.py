from datetime import datetime

import aiocsv
import aiofiles


async def write_order_info_to_csv(row):
    filename = f'orders/{datetime.now().date()}.csv'
    async with aiofiles.open(filename, 'w') as file:
        writer = aiocsv.AsyncWriter(file)
        await writer.writerow(row)