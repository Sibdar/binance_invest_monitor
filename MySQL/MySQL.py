import mysql.connector
import config

class MySQL():
    def __init__(self):
        self.cnx = mysql.connector.connect(user=config.user,
                                           password=config.password,
                                           host=config.host,
                                           database=config.database)
        self.cursor = self.cnx.cursor(buffered=True)

    def execute_sql(self, req):
        self.cursor.execute(req)
        self.cnx.commit()

    def insrt_into_prices(self, vals):
        insert_into_prices = f"""
                                INSERT INTO `curr_prices` (symbol, price, updated) VALUES {vals}
                                ON DUPLICATE KEY UPDATE price=VALUES(price), updated=VALUES(updated)                       
                              """
        self.execute_sql(insert_into_prices)

    def insrt_into_orders(self, vals):
        insert_into_orders = f"""
                                INSERT INTO `orders` (orderId, symbol, price, quantity, invested, 
                                                      status, side, order_date, order_time) VALUES {vals}
                                ON DUPLICATE KEY UPDATE orderId=orderId                      
                              """
        self.execute_sql(insert_into_orders)

    def insrt_into_my_assets(self, vals):
        insert_into_assets = f"""
                                INSERT INTO `my_assets` (asset, quantity, `balance (usd)`, date, time) VALUES {vals}
                                ON DUPLICATE KEY UPDATE 
                                                        quantity=VALUES(quantity), `balance (usd)`=VALUES(`balance (usd)`), 
                                                        date=VALUES(date), time=VALUES(time)                     
                              """
        self.execute_sql(insert_into_assets)

    def sel_last_usdtrub(self):
        sel_last_USDTRUB = """
                              SELECT quantity, symbol, order_date, order_time FROM orders 
                              WHERE symbol='USDTRUB' 
                              ORDER BY order_date DESC
                              LIMIT 1
                           """
        self.cursor.execute(sel_last_USDTRUB)
        return self.cursor.fetchone()

    def add_new_proj(self, vals):
        new_proj_req = f"""
                           INSERT INTO projects (project_name, budjet, goal, currency, create_date, create_time,
                                                 end_date)
                           VALUES {vals} 
                        """
        self.execute_sql(new_proj_req)

    def update_prj_detail_tab(self):
        cursor = self.cnx.cursor(buffered=True)
        sel_proj_data = """
                              select @prj_id:= project_id, @prj_curr:= currency, 
                                     @from_date:= create_date, @from_time:= create_time, 
                                     @to_date:= end_date, @to_time:= end_time from projects 
                              order by create_date desc, create_time desc 
                              limit 1; 
                        """
        cursor.execute(sel_proj_data)
        insrt_prj_det = """    
                            insert into project_details (order_id, project_id, symbol, qty, profit, 
                                                         curr, order_date, order_time, updated)                                      
                            select orders.orderId, @prj_id, orders.symbol, orders.quantity,
                                   curr_prices.price*orders.quantity-orders.invested,
                                   @prj_curr,
                                   orders.order_date, orders.order_time, NOW()
                            from orders inner join curr_prices on orders.symbol=curr_prices.symbol
                            where (orders.order_date between @from_date and @to_date) 
                                  and orders.order_time <> @from_time
                            order by orders.order_date desc, orders.order_time desc
                            ON DUPLICATE KEY UPDATE profit=curr_prices.price*orders.quantity-orders.invested,
                                                    updated=NOW();                   
                        """
        cursor.execute(insrt_prj_det)
        self.cnx.commit()

    def update_prj(self):
        cursor = self.cnx.cursor(buffered=True)
        upd_stat = """
                      -- calculate time passed in percents
                      select @cr_ts:= timestamp(create_date, create_time),
                             @end_ts:= timestamp(end_date, end_time),
                             @period_passed:= timestampdiff(minute, @cr_ts, now()),
                             @period_all:= timestampdiff(minute, @cr_ts, @end_ts)
                      from projects;
                      -- calculate total profit from crypto
                      select @prj_sum:= sum(profit) from project_details;
                      -- update fields in projects
                      update projects
                      set money_accum = @prj_sum,
                          `completed_at (%)` = (@prj_sum / projects.budjet) * 100,
                          `time_passed (%)` = @period_passed / @period_all * 100,
                          updated = now()
                    """
        for stat in upd_stat.split(';'):
            cursor.execute(stat + ';')
        self.cnx.commit()

    def get_prj_data(self, prj_name):
        sel_stat = f"""
                       select `project_name`, `money_accum`, `completed_at (%)`, `time_passed (%)`
                       from projects
                       where project_name='{prj_name}'
                    """
        self.execute_sql(sel_stat)
        return self.cursor.fetchone()


def main():
    db = MySQL()
    print(db.get_prj_data('Driving Licence'))
    # print(db.sel_last_usdtrub())




if __name__ == '__main__':
    main()