from unittest import TestCase

import pytest as pt


from api.v1.models import (
    db,
    Product,
    Stockpile
)
from tests.fixtures import api_test_client


@pt.mark.usefixtures("api_test_client")
class StockpileTestCase(TestCase):

    def test_get_return_200(self):
        data = {
            "title": "深入理解Java虚拟机（第3版）",
            "price": 129,
            "rate": 9.6,
            "description": "<p>这是一部从工作原理和工程实践两个维度深入剖析JVM的著作，是计算机领域公认的经典，繁体版在台湾也颇受欢迎。</p><p>自2011年上市以来，前两个版本累计印刷36次，销量超过30万册，两家主要网络书店的评论近90000条，内容上近乎零差评，是原创计算机图书领域不可逾越的丰碑，第3版在第2版的基础上做了重大修订，内容更丰富、实战性更强：根据新版JDK对内容进行了全方位的修订和升级，围绕新技术和生产实践新增逾10万字，包含近50%的全新内容，并对第2版中含糊、瑕疵和错误内容进行了修正。</p><p>全书一共13章，分为五大部分：</p><p>第一部分（第1章）走近Java</p><p>系统介绍了Java的技术体系、发展历程、虚拟机家族，以及动手编译JDK，了解这部分内容能对学习JVM提供良好的指引。</p><p>第二部分（第2~5章）自动内存管理</p><p>详细讲解了Java的内存区域与内存溢出、垃圾收集器与内存分配策略、虚拟机性能监控与故障排除等与自动内存管理相关的内容，以及10余个经典的性能优化案例和优化方法；</p><p>第三部分（第6~9章）虚拟机执行子系统</p><p>深入分析了虚拟机执行子系统，包括类文件结构、虚拟机类加载机制、虚拟机字节码执行引擎，以及多个类加载及其执行子系统的实战案例；</p><p>第四部分（第10~11章）程序编译与代码优化</p><p>详细讲解了程序的前、后端编译与优化，包括前端的易用性优化措施，如泛型、主动装箱拆箱、条件编译等的内容的深入分析；以及后端的性能优化措施，如虚拟机的热点探测方法、HotSpot 的即时编译器、提前编译器，以及各种常见的编译期优化技术；</p><p>第五部分（第12~13章）高效并发</p><p>主要讲解了Java实现高并发的原理，包括Java的内存模型、线程与协程，以及线程安全和锁优化。</p><p>全书以实战为导向，通过大量与实际生产环境相结合的案例分析和展示了解决各种Java技术难题的方案和技巧。</p>",
            "cover": "/static/cover/jvm3.jpg",
            "detail": "/static/desc/jvm3.jpg",
            # "specifications": [
            #     {
            #         "id": 1,
            #         "item": "作者",
            #         "value": "周志明"
            #     }
            # ]
        }

        product = Product(
            title=data["title"],
            price=data["price"],
            rate=data["rate"],
            description=data["description"],
            cover=data["cover"],
            detail=data["detail"]
        )
        db.session.add(product)
        db.session.commit()

        stockpile = Stockpile(
            product_id=product.id,
            amount=10,
            frozen=10
        )
        product.stockpiles.append(stockpile)
        db.session.add(product)
        db.session.commit()

        resp = self.client.get("/v1/products/stockpile/{}".format(product.id))
        assert resp.status_code == 200

    def test_patch_return_200(self):
        data = {
            "title": "深入理解Java虚拟机（第4版）",
            "price": 139,
            "rate": 9.6,
            "description": "<p>这是一部从工作原理和工程实践两个维度深入剖析JVM的著作，是计算机领域公认的经典，繁体版在台湾也颇受欢迎。</p><p>自2011年上市以来，前两个版本累计印刷36次，销量超过30万册，两家主要网络书店的评论近90000条，内容上近乎零差评，是原创计算机图书领域不可逾越的丰碑，第3版在第2版的基础上做了重大修订，内容更丰富、实战性更强：根据新版JDK对内容进行了全方位的修订和升级，围绕新技术和生产实践新增逾10万字，包含近50%的全新内容，并对第2版中含糊、瑕疵和错误内容进行了修正。</p><p>全书一共13章，分为五大部分：</p><p>第一部分（第1章）走近Java</p><p>系统介绍了Java的技术体系、发展历程、虚拟机家族，以及动手编译JDK，了解这部分内容能对学习JVM提供良好的指引。</p><p>第二部分（第2~5章）自动内存管理</p><p>详细讲解了Java的内存区域与内存溢出、垃圾收集器与内存分配策略、虚拟机性能监控与故障排除等与自动内存管理相关的内容，以及10余个经典的性能优化案例和优化方法；</p><p>第三部分（第6~9章）虚拟机执行子系统</p><p>深入分析了虚拟机执行子系统，包括类文件结构、虚拟机类加载机制、虚拟机字节码执行引擎，以及多个类加载及其执行子系统的实战案例；</p><p>第四部分（第10~11章）程序编译与代码优化</p><p>详细讲解了程序的前、后端编译与优化，包括前端的易用性优化措施，如泛型、主动装箱拆箱、条件编译等的内容的深入分析；以及后端的性能优化措施，如虚拟机的热点探测方法、HotSpot 的即时编译器、提前编译器，以及各种常见的编译期优化技术；</p><p>第五部分（第12~13章）高效并发</p><p>主要讲解了Java实现高并发的原理，包括Java的内存模型、线程与协程，以及线程安全和锁优化。</p><p>全书以实战为导向，通过大量与实际生产环境相结合的案例分析和展示了解决各种Java技术难题的方案和技巧。</p>",
            "cover": "/static/cover/jvm3.jpg",
            "detail": "/static/desc/jvm3.jpg",
            # "specifications": [
            #     {
            #         "id": 1,
            #         "item": "作者",
            #         "value": "周志明"
            #     }
            # ]
        }

        product = Product(
            title=data["title"],
            price=data["price"],
            rate=data["rate"],
            description=data["description"],
            cover=data["cover"],
            detail=data["detail"]
        )
        db.session.add(product)
        db.session.commit()

        stockpile = Stockpile(
            product_id=product.id,
            amount=10,
            frozen=10
        )
        product.stockpiles.append(stockpile)
        db.session.add(product)
        db.session.commit()

        json_data = dict(
            product_id=product.id,
            amount=1,
            frozen=0
        )
        resp = self.client.patch("/v1/products/stockpile/{}".format(product.id), json=json_data)
        assert resp.status_code == 200