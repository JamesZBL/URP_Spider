# -*- coding:utf-8 -*-
""" 
@author:James
Created on:18-2-8 17:01
"""

import gevent


class A:
	def f(self, repeat):
		for i in range(repeat):
			print(i)
			gevent.sleep(0)


class B:
	def run(self):
		app = A()
		appb = A()
		appc = A()
		gevent.spawn(app.f(100)).join()
		gevent.spawn(appb.f(100)).join()
		gevent.spawn(appc.f(100)).join()


if __name__ == '__main__':
	app = B()
	app.run()
