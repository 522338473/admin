from crm import models

class CNM(object):
    users = None
    iter_users = None
    reset_status = False
    rollback_list = []

    @classmethod
    def fetch_users(cls):
        sales_list = models.SaleRank.objects.all().order_by('-weight')
        sales = []     #[销售者，销售量，销售顾问ID]    =========》最后要返回ID|需要的是ID ==》[['张磊', 3, 11], ['安琪', 2, 5]]
        count = 0
        while True:
            '''
            循环处理数据--->得到[x,xx,xxx,xx,x]  =====>最终返回
            '''
            flag = False
            for row in sales_list:
                if count < row.num:
                    sales.append(row.user_id)
                    flag = True
            count +=1
            if not flag:
                break
        cls.users = sales
        print(cls.users,"======================>")





        # v = [短期, 番禺, 富贵, 秦晓, 短期, 番禺, 富贵, 秦晓, 番禺, 富贵, 秦晓, 秦晓, 秦晓, 秦晓, 秦晓, 秦晓, 秦晓...]



    # 返回一个用户ID列表

    @classmethod
    def get_sale_id(cls):
        if not cls.users:
            cls.fetch_users()
        if not cls.iter_users:
            cls.iter_users = iter(cls.users)
            print(cls.iter_users,'===========>')
        try:
            user_id = next(cls.iter_users)

        except StopIteration as e:
            if cls.reset_status:
                cls.fetch_users()
                cls.reset_status = False
            cls.iter_users = iter(cls.users)
            user_id = cls.get_sale_id()
        return user_id
        #需要销售者ID

    @classmethod
    def reset(cls):
        cls.reset_status = True