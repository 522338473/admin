import redis
from crm import models

POOL = redis.ConnectionPool(host="47.93.4.198",port=6379,password="123123")
CONN = redis.Redis(connection_pool=POOL)


class CNM(object):

    @classmethod
    def fetch_users(cls):
        sales = models.SaleRank.objects.all().order_by('-weight')
        sale_id_list = []     #[销售者，销售量，销售顾问ID]    =========》最后要返回ID|需要的是ID ==》[['张磊', 3, 11], ['安琪', 2, 5]]
        count = 0
        while True:
            '''
            循环处理数据--->得到[x,xx,xxx,xx,x]  =====>最终返回
            '''
            flag = False
            for row in sales:
                if count < row.num:
                    sale_id_list.append(row.user_id)
                    flag = True
            count +=1
            if not flag:
                break
        if sale_id_list:
            CONN.rpush("sale_id_list",*sale_id_list)
            CONN.rpush("sale_id_list_origin",*sale_id_list)
            return True
        return False

        # v = [短期, 番禺, 富贵, 秦晓, 短期, 番禺, 富贵, 秦晓, 番禺, 富贵, 秦晓, 秦晓, 秦晓, 秦晓, 秦晓, 秦晓, 秦晓...]



    # 返回一个用户ID列表

    @classmethod
    def get_sale_id(cls):
        sale_id_origin_count = CONN.llen("sale_id_list_origin")
        if not sale_id_origin_count:
            status = cls.fetch_users()
            if not status:
                return None
        user_id = CONN.lpop("sale_id_list")
        if user_id:
            return user_id
        #需要销售者ID
        reset = CONN.get("sale_id_reset")
        if reset:
            CONN.delete("sale_id_list_origin")
            status = cls.fetch_users()
            if not status:
                return None
            CONN.delete("sale_id_reset")
            return CONN.lpop("sale_id_list")
        else:
            ct = CONN.llen("sale_id_list_origin")
            for i in range(ct):
                v = CONN.lindex("sale_id_list_origin",i)
                CONN.rpush("sale_id_list",v)
            return CONN.lpop("sale_id_list")



    @classmethod
    def reset(cls):
        CONN.set("sale_id_reset",1)

    @classmethod
    def rollback(cls,nid):
        CONN.lpush("sale_id_list", nid)