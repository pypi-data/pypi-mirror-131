from tqdm import tqdm
import numpy
from enum import IntEnum
import os
import sys
import csv
import time
import json

from multiprocessing import Process, Queue
import queue

Q = Queue()

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

lbar		= None
server		= None

file_log	= None

norm_log	= []
wnorm_log	= []
obj_log		= []
time_log	= []
start_time	= None
state		= None

STATUS_PORT = 10000
if os.environ.get('PX_STATUS_PORT') is not None:
	STATUS_PORT = int(os.environ['PX_STATUS_PORT'])

class WSStatus(WebSocket):

	last_state = None

	def handleMessage(self):
		if self.data == 'poll':
			try:
				elapsed  = Q.get(True,1)
				cur_iter = Q.get(True,1)
				max_iter = Q.get(True,1)
				best_nrm = Q.get(True,1)
				best_obj = Q.get(True,1)
				best_wnrm= Q.get(True,1)
				
				sdata = { "empty": False, "iter": cur_iter, "iter_max": max_iter, "elapsed": elapsed, "objective": best_obj, "grad_norm": best_nrm, "weight_norm": best_wnrm }

				sjson = None
				
				try:
					sjson = json.dumps(sdata)
				except:	
					print("ERR:",sys.exc_info())
				
				self.last_state = sjson
				
			except:
				print("ERR:",sys.exc_info())
				if self.last_state is None:
					sdata = { "empty": True }
					self.last_state = json.dumps(sdata)
				else:
					pass

			self.sendMessage(self.last_state)

	def handleConnected(self):
		print(self.address, 'connected')

	def handleClose(self):
		print(self.address, 'closed')

def __wsrun(port,start_time,state,norm_log,wnorm_log,obj_log,time_log):
	global server
	server = SimpleWebSocketServer('', port, WSStatus)
	server.serveforever()

STATUS_PROVIDER_PROCESS = None
	
class OptimizerHookType(IntEnum):
	quite = 0
	quite_logfile = 1
	plain = 2
	plain_logfile = 3
	tqdm = 4
	tqdm_logfile = 5

def __optimizer_hook(state_p,hooktype):
	global lbar
	
	global file_log
	
	global norm_log
	global wnorm_log
	global obj_log
	global time_log
	global start_time
	global state
	
	global server

	state = state_p.contents
	
	if start_time is None:
		start_time = time.time()
	
	global STATUS_PROVIDER_PROCESS
	
	if os.environ.get('PX_STATUS_PROVIDER') is not None and STATUS_PROVIDER_PROCESS is None:
		STATUS_PROVIDER_PROCESS = Process(target=__wsrun, args=(STATUS_PORT,start_time,state,norm_log,wnorm_log,obj_log,time_log))
		STATUS_PROVIDER_PROCESS.start()

	if hooktype > 3 and lbar is None:
		lbar = tqdm(total=state.max_iterations)

	if hooktype % 2 == 1 and file_log is None:
		file_log = open('px_'+str(int(start_time))+'.log','w')

	wnrm = numpy.linalg.norm(state.best_weights)
	
	norm_log.append(state.best_norm)
	wnorm_log.append(wnrm)
	obj_log.append(state.best_obj)
	
	now = time.time()
	time_log.append(now)

	if STATUS_PROVIDER_PROCESS is not None:
		Q.put(now-start_time)	
		Q.put(state.iteration)
		Q.put(state.max_iterations)
		Q.put(state.best_norm)
		Q.put(state.best_obj)
		Q.put(wnrm)

	log_str = "{:.4f}".format(now-start_time) + '\t' + str(state.iteration) + '\t' + str(state.best_obj) + '\t' + str(state.best_norm) + '\t' + str(wnrm)
	
	if hooktype == 2 or hooktype == 3:
		print(log_str)
		
	if hooktype % 2 == 1:
		file_log.write(log_str+'\n')
		
	if hooktype == 4 or hooktype == 5:
		lbar.set_description( "OPT;" + "{:.4f};{:.4f}".format(state.best_norm,state.best_obj) )
		lbar.update(1)

	if state.iteration == state.max_iterations:
		if hooktype % 2 == 1:
			file_log.close()

		if hooktype > 3:
			lbar.close()
			lbar = None
			
		file_log = None
		start_time = None
		norm_log.clear()
		wnorm_log.clear()
		obj_log.clear()
		
		if STATUS_PROVIDER_PROCESS is not None:
			print('TRY TO EXIT..')
			STATUS_PROVIDER_PROCESS.join(5)
			if STATUS_PROVIDER_PROCESS.is_alive():
				STATUS_PROVIDER_PROCESS.terminate()
			print('FAILED?')

def opt_progress_hook_quite(state_p):
	__optimizer_hook(state_p,OptimizerHookType.quite)
	
def opt_progress_hook_quite_logfile(state_p):
	__optimizer_hook(state_p,OptimizerHookType.quite_logfile)
	
def opt_progress_hook_plain(state_p):
	__optimizer_hook(state_p,OptimizerHookType.plain)
	
def opt_progress_hook_plain_logfile(state_p):
	__optimizer_hook(state_p,OptimizerHookType.plain_logfile)
	
def opt_progress_hook_tqdm(state_p):
	__optimizer_hook(state_p,OptimizerHookType.tqdm)
	
def opt_progress_hook_tqdm_logfile(state_p):
	__optimizer_hook(state_p,OptimizerHookType.tqdm_logfile)

def opt_progress_hook(state_p):
	__optimizer_hook(state_p,OptimizerHookType.tqdm)

def generic_progress_hook(_cur,_tot,_nam):
	if type(_nam) is not str:
		_nam = _nam.decode('utf-8')

	global lbar

	if lbar is None:
		lbar = tqdm(total=_tot, desc=_nam, position=0, leave=True)

	lbar.update(_cur - lbar.n)
	lbar.set_description(_nam)

	if _cur == _tot:
		lbar.close()
		lbar = None
	
def genfromstrcsv(filename, targets=None, has_header=True):
	N = 0
	n = None
	values = None

	csv_data = open(filename)
	csv_reader = csv.reader(csv_data)
	header = next(csv_reader)
	n = len(header)

	if targets is None:
		targets = range(n)
	values = dict()

	if not has_header:
		N = N+1
		for i in targets:
			if i not in values.keys():
				values[i] = set()
			values[i].add(header[i])

	for row in csv_reader:
		N = N+1
		for i in targets:
			if i not in values.keys():
				values[i] = set()
			values[i].add(row[i])

	vmaps  = dict()
	rvmaps = dict()

	for i in targets:
		j = 0

		if i not in vmaps.keys():
			vmaps[i] = dict()
			rvmaps[i] = dict()

		for v in values[i]:
			vmaps[i][v] = j
			rvmaps[i][j] = v

			j = j+1

	result = numpy.zeros((N,len(targets)), dtype=numpy.uint16)


	csv_data.seek(0)

	csv_reader = csv.reader(csv_data)
	header = next(csv_reader)

	if targets is None:
		targets = range(n)

	I = 0
	if not has_header:
		J = 0
		for i in targets:
			result[I,J] = vmaps[i][header[i]]
			J = J + 1
		I = 1

	for row in csv_reader:
		J = 0
		for i in targets:
			result[I,J] = vmaps[i][row[i]]
			J = J + 1
		I = I + 1

	return result, rvmaps
	
class ModelQUBOmixin:

	def export_qubo(self):
		dim = int(self.ysum)
		penalty = numpy.sum(numpy.partition(self.weights,-self.graph.edges)[-self.graph.edges:])
		Q = penalty * numpy.ones(dim**2).reshape(dim,dim)
		
		for v in range(self.graph.nodes):
			Q[v,v] = 0

		for e in range(self.graph.edges):
		
			# (s,t)
			s = self.graph.edgelist[e][0]
			t = self.graph.edgelist[e][1]
			
			si = self.offsets[s]
			ti = self.offsets[t]
		
			# w_(s,t)
			w = self.slice_edge(e,self.weights)

			for sx in range(self.states[s]):
				for tx in range(self.states[t]):
					print(s,sx,t,tx)
					idx = int(sx * self.states[t] + tx)
					wsxtx = w[idx]
					Q[si,ti] = -wsxtx
					Q[ti,si] = -wsxtx
		return Q

import onnx
from onnx import helper, TensorProto

class ModelONNXmixin:

	def gamma_sampler_consts(self,alpha):
		ld = 1.0334 - 0.0766 * numpy.exp(2.2942 * alpha)
		la = (2**alpha) * (1.0 - numpy.exp(-ld/2.0))**alpha
		lb = alpha * (ld**(alpha-1)) * numpy.exp(-ld)
		lc = la+lb
		return la,lb,lc,ld,1.0/alpha,alpha * (ld**(alpha-1.0)),(alpha-1.0),2**(alpha-1.0),1.0-alpha

	def export_onnx(self, fname, probmodel=False, perturb=False, iterations=None, temperature=1.0):

	# INT8 to INT32 seem to by unsupported by onnx
	#		if self._Model_incomplete__idxtype == numpy.uint8:
	#			ITYPE = TensorProto.INT8
	#		elif self._Model_incomplete__idxtype == numpy.uint16:
	#			ITYPE = TensorProto.INT16
	#		elif self._Model_incomplete__idxtype == numpy.uint32:
	#			ITYPE = TensorProto.INT32
		if self._Model_incomplete__idxtype == numpy.uint64:
			ITYPE = TensorProto.INT64
		else:
			raise TypeError('Index type '+str(self._Model_incomplete__idxtype)+' not supported for ONNX export.')

		if self._Model_incomplete__valtype == numpy.float32:
			DTYPE = TensorProto.FLOAT
		elif self._Model_incomplete__valtype == numpy.float64:
			DTYPE = TensorProto.DOUBLE
		else:
			raise TypeError('Value type '+str(self._Model_incomplete__idxtype)+' not supported for ONNX export.')

		################################################################################
		# INIT
		################################################################################

		Ne  = {}
		NeE = {}
		for v in range(self.graph.nodes):
			Ne[v]  = []
			NeE[v] = []

		ONNX_OP_LIST = []

		MAPv   = []
		PROBv  = []

		################################################################################
		# MODEL WEIGHTS, ONE ONNX-NODE FOR EACH EDGE WEIGHT VECTOR
		################################################################################

		CONSTANT_ONEid = 'CONSTANT_ONE'
		CONSTANT_ONEv = numpy.array([1],dtype=self._Model_incomplete__idxtype)
		CONSTANT_ONEn = helper.make_node(
			'Constant',
			inputs=[],
			outputs=[CONSTANT_ONEid],
		 	value=helper.make_tensor(
				name=CONSTANT_ONEid+'_content',
				data_type=ITYPE,
				dims=CONSTANT_ONEv.shape,
				vals=CONSTANT_ONEv.flatten(),
			),
		)
		ONNX_OP_LIST.append(CONSTANT_ONEn)
		
		CONSTANT_ONE_Fid = 'CONSTANT_ONE_F'
		CONSTANT_ONE_Fv = numpy.array([1.0],dtype=self._Model_incomplete__valtype)
		CONSTANT_ONE_Fn = helper.make_node(
			'Constant',
			inputs=[],
			outputs=[CONSTANT_ONE_Fid],
		 	value=helper.make_tensor(
				name=CONSTANT_ONE_Fid+'_content',
				data_type=DTYPE,
				dims=CONSTANT_ONE_Fv.shape,
				vals=CONSTANT_ONE_Fv.flatten(),
			),
		)
		ONNX_OP_LIST.append(CONSTANT_ONE_Fn)
		
		CONSTANT_nONE_Fid = 'CONSTANT_nONE_F'
		CONSTANT_nONE_Fv = numpy.array([-1.0],dtype=self._Model_incomplete__valtype)
		CONSTANT_nONE_Fn = helper.make_node(
			'Constant',
			inputs=[],
			outputs=[CONSTANT_nONE_Fid],
		 	value=helper.make_tensor(
				name=CONSTANT_nONE_Fid+'_content',
				data_type=DTYPE,
				dims=CONSTANT_nONE_Fv.shape,
				vals=CONSTANT_nONE_Fv.flatten(),
			),
		)
		ONNX_OP_LIST.append(CONSTANT_nONE_Fn)
		
		CONSTANT_TWO_Fid = 'CONSTANT_TWO_F'
		CONSTANT_TWO_Fv = numpy.array([2.0],dtype=self._Model_incomplete__valtype)
		CONSTANT_TWO_Fn = helper.make_node(
			'Constant',
			inputs=[],
			outputs=[CONSTANT_TWO_Fid],
		 	value=helper.make_tensor(
				name=CONSTANT_TWO_Fid+'_content',
				data_type=DTYPE,
				dims=CONSTANT_TWO_Fv.shape,
				vals=CONSTANT_TWO_Fv.flatten(),
			),
		)
		ONNX_OP_LIST.append(CONSTANT_TWO_Fn)
		
		CONSTANT_nTWO_Fid = 'CONSTANT_nTWO_F'
		CONSTANT_nTWO_Fv = numpy.array([-2.0],dtype=self._Model_incomplete__valtype)
		CONSTANT_nTWO_Fn = helper.make_node(
			'Constant',
			inputs=[],
			outputs=[CONSTANT_nTWO_Fid],
		 	value=helper.make_tensor(
				name=CONSTANT_nTWO_Fid+'_content',
				data_type=DTYPE,
				dims=CONSTANT_nTWO_Fv.shape,
				vals=CONSTANT_nTWO_Fv.flatten(),
			),
		)
		ONNX_OP_LIST.append(CONSTANT_nTWO_Fn)

		if perturb:
			S = 10
			GAMMA_TRIALS = 8
			
			kappa = self.graph.edges

			logSid = 'logS'
			logSval = numpy.array([numpy.log(S)])
			logSn = helper.make_node(
				'Constant',
				inputs=[],
				outputs=[logSid],
			 	value=helper.make_tensor(
					name=logSid+'_content',
					data_type=DTYPE,
					dims=logSval.shape,
					vals=logSval.flatten(),
				),
			)
			ONNX_OP_LIST.append(logSn)
			
			kinvid = 'kappa_inv'
			kinvval = numpy.array([temperature/kappa])
			kinvn = helper.make_node(
				'Constant',
				inputs=[],
				outputs=[kinvid],
			 	value=helper.make_tensor(
					name=kinvid+'_content',
					data_type=DTYPE,
					dims=kinvval.shape,
					vals=kinvval.flatten(),
				),
			)
			ONNX_OP_LIST.append(kinvn)
			
			GSC  = self.gamma_sampler_consts(1.0/kappa)
			GSCl = []

			for ii in range(len(GSC)):
				GSCid  = 'GSC_'+str(ii)
				GSCval = numpy.array([GSC[ii]])
				GSCn   = helper.make_node(
					'Constant',
					inputs=[],
					outputs=[GSCid],
				 	value=helper.make_tensor(
						name=GSCid+'_content',
						data_type=DTYPE,
						dims=GSCval.shape,
						vals=GSCval.flatten(),
					),
				)
				if ii > 1: # GSC_0 and GSC_1 are unused
					ONNX_OP_LIST.append(GSCn)
					GSCl.append(GSCid)
			
			C1id  = 'gamma_sampler_comparison_1'
			C1val = numpy.array([GSC[0]/(GSC[0]+GSC[1])])
			C1n   = helper.make_node(
				'Constant',
				inputs=[],
				outputs=[C1id],
			 	value=helper.make_tensor(
					name=C1id+'_content',
					data_type=DTYPE,
					dims=C1val.shape,
					vals=C1val.flatten(),
				),
			)
			ONNX_OP_LIST.append(C1n)
			
			SCALEl = []
			
			for si in range(S):
				SCALEid = 'SCALE_s'+str(si)
				SCALEval = numpy.array([kappa/(si+1.0)])
				SCALEn = helper.make_node(
					'Constant',
					inputs=[],
					outputs=[SCALEid],
				 	value=helper.make_tensor(
						name=SCALEid+'_content',
						data_type=DTYPE,
						dims=SCALEval.shape,
						vals=SCALEval.flatten(),
					),
				)
				ONNX_OP_LIST.append(SCALEn)
				SCALEl.append(SCALEid)

		for e in range(self.graph.edges):

			s = self.graph.edgelist[e][0]
			t = self.graph.edgelist[e][1]
			
		 	# populate neighborhoods
			if not t in Ne[s]:
				Ne[s].append(t)
				NeE[s].append(e)
			if not s in Ne[t]:
				Ne[t].append(s)
				NeE[t].append(e)
			
			Ys = int(self.states[s])
			Yt = int(self.states[t])
			
			WEIGHTSid = 'WEIGHTS_'+str(e)
			WEIGHTS = helper.make_tensor_value_info(WEIGHTSid, DTYPE, shape=(Ys,Yt))	
			WEIGHTSval = self.slice_edge(e,self.weights).reshape(Ys,Yt)
			WEIGHTSn = helper.make_node(
				'Constant',
				inputs=[],
				outputs=[WEIGHTSid],
			 	value=helper.make_tensor(
					name=WEIGHTSid+'_content',
					data_type=DTYPE,
					dims=WEIGHTSval.shape,
					vals=WEIGHTSval.flatten(),
				),
			)
			ONNX_OP_LIST.append(WEIGHTSn)
			
			if perturb:
				
				SoG_I = []

				for si in range(S):
					#PERTURBid = 'PERTURB_'+str(e)+'_s'+str(si)
					#PERTURBn = helper.make_node(
					#	'RandomNormal',
					#	inputs=[],
					#	outputs=[PERTURBid],
					#	shape=(Ys,Yt),
					#	scale=numpy.sqrt(kappa/((1.0+si)*2)),
					#	dtype=DTYPE,
					#)
					#ONNX_OP_LIST.append(PERTURBn)
					
					### This is Algorithm 3 from "Debasis Kundu1 and Rameshwar D. Gupta. A Convenient Way of Generating Gamma Random Variables Using Generalized Exponential Distribution"
					
					### DRAW U (Step 1)
					
					Uid = 'U_'+str(e)+'_s'+str(si)
					Un = helper.make_node(
						'RandomUniform',
						inputs=[],
						outputs=[Uid],
						shape=(Ys,Yt,GAMMA_TRIALS),
						dtype=DTYPE,
					)
					ONNX_OP_LIST.append(Un)
					
					### COMPUTE X1 = -2ln(1-(cU)^(1/alpha)/2)

					X1a_id = 'X1a_'+str(e)+'_s'+str(si)
					X1a_n = helper.make_node(
						'Mul',
						inputs=[GSCl[2],Uid],
						outputs=[X1a_id],
					)
					ONNX_OP_LIST.append(X1a_n)
					
					X1b_id = 'X1b_'+str(e)+'_s'+str(si)
					X1b_n = helper.make_node(
						'Pow',
						inputs=[X1a_id,GSCl[4]],
						outputs=[X1b_id],
					)
					ONNX_OP_LIST.append(X1b_n)
					
					X1c_id = 'X1c_'+str(e)+'_s'+str(si)
					X1c_n = helper.make_node(
						'Div',
						inputs=[X1b_id,CONSTANT_TWO_Fid],
						outputs=[X1c_id],
					)
					ONNX_OP_LIST.append(X1c_n)
					
					X1d_id = 'X1d_'+str(e)+'_s'+str(si)
					X1d_n = helper.make_node(
						'Sub',
						inputs=[CONSTANT_ONE_Fid,X1c_id],
						outputs=[X1d_id],
					)
					ONNX_OP_LIST.append(X1d_n)
					
					X1e_id = 'X1e_'+str(e)+'_s'+str(si)
					X1e_n = helper.make_node(
						'Log',
						inputs=[X1d_id],
						outputs=[X1e_id],
					)
					ONNX_OP_LIST.append(X1e_n)
					
					X1_id = 'X1_'+str(e)+'_s'+str(si)
					X1_n = helper.make_node(
						'Mul',
						inputs=[CONSTANT_nTWO_Fid,X1e_id],
						outputs=[X1_id],
					)
					ONNX_OP_LIST.append(X1_n)
					
					### COMPUTE X2 = -ln(c(1-U)/(alpha*d^(alpha-1)))
					
					X2a_id = 'X2a_'+str(e)+'_s'+str(si)
					X2a_n = helper.make_node(
						'Sub',
						inputs=[CONSTANT_ONE_Fid,Uid],
						outputs=[X2a_id],
					)
					ONNX_OP_LIST.append(X2a_n)
					
					X2b_id = 'X2b_'+str(e)+'_s'+str(si)
					X2b_n = helper.make_node(
						'Mul',
						inputs=[GSCl[2],X2a_id],
						outputs=[X2b_id],
					)
					ONNX_OP_LIST.append(X2b_n)
					
					X2c_id = 'X2c_'+str(e)+'_s'+str(si)
					X2c_n = helper.make_node(
						'Div',
						inputs=[X2b_id,GSCl[5]],
						outputs=[X2c_id],
					)
					ONNX_OP_LIST.append(X2c_n)

					X2d_id = 'X2d_'+str(e)+'_s'+str(si)
					X2d_n = helper.make_node(
						'Log',
						inputs=[X2c_id],
						outputs=[X2d_id],
					)
					ONNX_OP_LIST.append(X2d_n)
					
					X2_id = 'X2_'+str(e)+'_s'+str(si)
					X2_n = helper.make_node(
						'Mul',
						inputs=[CONSTANT_nONE_Fid,X2d_id],
						outputs=[X2_id],
					)
					ONNX_OP_LIST.append(X2_n)
					
					### CHECK CONDITION wrt U (Step 2)
					
					COMP1id = 'COMP1_'+str(e)+'_s'+str(si)
					COMP1n = helper.make_node(
						'LessOrEqual',
						inputs=[Uid,C1id],
						outputs=[COMP1id],
					)
					ONNX_OP_LIST.append(COMP1n)
					
					COMP1_Fid = 'COMP1_F_'+str(e)+'_s'+str(si)
					COMP1_Fn = helper.make_node(
						'Cast',
						inputs=[COMP1id],
						outputs=[COMP1_Fid],
						to=DTYPE,
					)
					ONNX_OP_LIST.append(COMP1_Fn)
					
					COMP1INV_Fid = 'COMP1INV_F_'+str(e)+'_s'+str(si)
					COMP1INV_Fn = helper.make_node(
						'Sub',
						inputs=[CONSTANT_ONE_Fid,COMP1_Fid],
						outputs=[COMP1INV_Fid],
					)
					ONNX_OP_LIST.append(COMP1INV_Fn)
					
					RC1_id = 'RC1_'+str(e)+'_s'+str(si)
					RC1_n = helper.make_node(
						'Mul',
						inputs=[COMP1_Fid,X1_id],
						outputs=[RC1_id],
					)
					ONNX_OP_LIST.append(RC1_n)
					
					RC2_id = 'RC2_'+str(e)+'_s'+str(si)
					RC2_n = helper.make_node(
						'Mul',
						inputs=[COMP1INV_Fid,X2_id],
						outputs=[RC2_id],
					)
					ONNX_OP_LIST.append(RC2_n)
					
					X_id = 'X_'+str(e)+'_s'+str(si)
					X_n = helper.make_node(
						'Add',
						inputs=[RC1_id,RC2_id],
						outputs=[X_id],
					)
					ONNX_OP_LIST.append(X_n)
					
					### COMPUTE X^(alpha-1) exp(-X/2) / (2^(alpha-1) (1 - exp(-X/2)^(alpha-1)))
					
					T1a_id = 'T1a_'+str(e)+'_s'+str(si)
					T1a_n = helper.make_node(
						'Pow',
						inputs=[X_id,GSCl[6]],
						outputs=[T1a_id],
					)
					ONNX_OP_LIST.append(T1a_n)
					
					T1b_id = 'T1b_'+str(e)+'_s'+str(si)
					T1b_n = helper.make_node(
						'Div',
						inputs=[X_id,CONSTANT_nTWO_Fid],
						outputs=[T1b_id],
					)
					ONNX_OP_LIST.append(T1b_n)
					
					T1c_id = 'T1c_'+str(e)+'_s'+str(si)
					T1c_n = helper.make_node(
						'Exp',
						inputs=[T1b_id],
						outputs=[T1c_id],
					)
					ONNX_OP_LIST.append(T1c_n)
					
					T1d_id = 'T1d_'+str(e)+'_s'+str(si)
					T1d_n = helper.make_node(
						'Mul',
						inputs=[T1a_id,T1c_id],
						outputs=[T1d_id],
					)
					ONNX_OP_LIST.append(T1d_n)
					
					T1e_id = 'T1e_'+str(e)+'_s'+str(si)
					T1e_n = helper.make_node(
						'Sub',
						inputs=[CONSTANT_ONE_Fid,T1c_id],
						outputs=[T1e_id],
					)
					ONNX_OP_LIST.append(T1e_n)
					
					T1f_id = 'T1f_'+str(e)+'_s'+str(si)
					T1f_n = helper.make_node(
						'Pow',
						inputs=[T1e_id,GSCl[6]],
						outputs=[T1f_id],
					)
					ONNX_OP_LIST.append(T1f_n)
					
					T1g_id = 'T1g_'+str(e)+'_s'+str(si)
					T1g_n = helper.make_node(
						'Mul',
						inputs=[GSCl[7],T1f_id],
						outputs=[T1g_id],
					)
					ONNX_OP_LIST.append(T1g_n)
					
					T1_id = 'T1_'+str(e)+'_s'+str(si)
					T1_n = helper.make_node(
						'Div',
						inputs=[T1d_id,T1g_id],
						outputs=[T1_id],
					)
					ONNX_OP_LIST.append(T1_n)

					### COMPUTE (d/X)**(1-alpha)
					
					T2a_id = 'T2a_'+str(e)+'_s'+str(si)
					T2a_n = helper.make_node(
						'Div',
						inputs=[GSCl[3],X_id],
						outputs=[T2a_id],
					)
					ONNX_OP_LIST.append(T2a_n)
					
					T2_id = 'T2_'+str(e)+'_s'+str(si)
					T2_n = helper.make_node(
						'Pow',
						inputs=[T2a_id,GSCl[8]],
						outputs=[T2_id],
					)
					ONNX_OP_LIST.append(T2_n)

					### CHECK CONDITION wrt V (Step 3)
					
					Vid = 'V_'+str(e)+'_s'+str(si)
					Vn = helper.make_node(
						'RandomUniform',
						inputs=[],
						outputs=[Vid],
						shape=(Ys,Yt,GAMMA_TRIALS),
						dtype=DTYPE,
					)
					ONNX_OP_LIST.append(Vn)
					
					Xlted_id = 'Xlted'+str(e)+'_s'+str(si)
					Xlted_n = helper.make_node(
						'LessOrEqual',
						inputs=[X_id,GSCl[3]],
						outputs=[Xlted_id],
					)
					ONNX_OP_LIST.append(Xlted_n)
					
					Xlted_Fid = 'Xlted_F_'+str(e)+'_s'+str(si)
					Xlted_Fn = helper.make_node(
						'Cast',
						inputs=[Xlted_id],
						outputs=[Xlted_Fid],
						to=DTYPE,
					)
					ONNX_OP_LIST.append(Xlted_Fn)
					
					XltedINV_Fid = 'XltedINV_F_'+str(e)+'_s'+str(si)
					XltedINV_Fn = helper.make_node(
						'Sub',
						inputs=[CONSTANT_ONE_Fid,Xlted_Fid],
						outputs=[XltedINV_Fid],
					)
					ONNX_OP_LIST.append(XltedINV_Fn)
					
					VlteT1_id = 'VlteT1'+str(e)+'_s'+str(si)
					VlteT1_n = helper.make_node(
						'LessOrEqual',
						inputs=[Vid,T1_id],
						outputs=[VlteT1_id],
					)
					ONNX_OP_LIST.append(VlteT1_n)
					
					VlteT1_Fid = 'VlteT1_F_'+str(e)+'_s'+str(si)
					VlteT1_Fn = helper.make_node(
						'Cast',
						inputs=[VlteT1_id],
						outputs=[VlteT1_Fid],
						to=DTYPE,
					)
					ONNX_OP_LIST.append(VlteT1_Fn)
					
					VlteT2_id = 'VlteT2'+str(e)+'_s'+str(si)
					VlteT2_n = helper.make_node(
						'LessOrEqual',
						inputs=[Vid,T2_id],
						outputs=[VlteT2_id],
					)
					ONNX_OP_LIST.append(VlteT2_n)
					
					VlteT2_Fid = 'VlteT2_F_'+str(e)+'_s'+str(si)
					VlteT2_Fn = helper.make_node(
						'Cast',
						inputs=[VlteT2_id],
						outputs=[VlteT2_Fid],
						to=DTYPE,
					)
					ONNX_OP_LIST.append(VlteT2_Fn)
					
					GS_FINAL1_id = 'GS_FINAL1_'+str(e)+'_s'+str(si)
					GS_FINAL1_Fn = helper.make_node(
						'Mul',
						inputs=[Xlted_Fid,VlteT1_Fid],
						outputs=[GS_FINAL1_id],
					)
					ONNX_OP_LIST.append(GS_FINAL1_Fn)
					
					GS_FINAL1b_id = 'GS_FINAL1b_'+str(e)+'_s'+str(si)
					GS_FINAL1b_Fn = helper.make_node(
						'Mul',
						inputs=[GS_FINAL1_id,X_id],
						outputs=[GS_FINAL1b_id],
					)
					ONNX_OP_LIST.append(GS_FINAL1b_Fn)
					
					GS_FINAL2_id = 'GS_FINAL2_'+str(e)+'_s'+str(si)
					GS_FINAL2_Fn = helper.make_node(
						'Mul',
						inputs=[XltedINV_Fid,VlteT2_Fid],
						outputs=[GS_FINAL2_id],
					)
					ONNX_OP_LIST.append(GS_FINAL2_Fn)
					
					GS_FINAL2b_id = 'GS_FINAL2b_'+str(e)+'_s'+str(si)
					GS_FINAL2b_Fn = helper.make_node(
						'Mul',
						inputs=[GS_FINAL2_id,X_id],
						outputs=[GS_FINAL2b_id],
					)
					ONNX_OP_LIST.append(GS_FINAL2b_Fn)
					
					GS_FINAL_id = 'GS_FINAL_'+str(e)+'_s'+str(si)
					GS_FINAL_Fn = helper.make_node(
						'Add',
						inputs=[GS_FINAL1b_id,GS_FINAL2b_id],
						outputs=[GS_FINAL_id],
					)
					ONNX_OP_LIST.append(GS_FINAL_Fn)
					
					GS_REDUCED_id = 'GS_REDUCED_'+str(e)+'_s'+str(si)
					GS_REDUCED_Fn = helper.make_node(
						'ReduceMax',
						inputs=[GS_FINAL_id],
						outputs=[GS_REDUCED_id],
						keepdims=0,
						axes=[2],
					)
					ONNX_OP_LIST.append(GS_REDUCED_Fn)
					
					### SCALE GAMMA VAR

					GAMMA_SAMPLE_id = 'GAMMA_SAMPLE_'+str(e)+'_s'+str(si)
					GAMMA_SAMPLE_n = helper.make_node(
						'Mul',
						inputs=[SCALEl[si],GS_REDUCED_id],
						outputs=[GAMMA_SAMPLE_id],
					)
					ONNX_OP_LIST.append(GAMMA_SAMPLE_n)
					
					### SAMPLING DONE - SUBTRACT log(S)
					
					SOGbid = 'SOGb_'+str(e)+'_s'+str(si)
					SOGbn = helper.make_node(
						'Sub',
						inputs=[GAMMA_SAMPLE_id,logSid],
						outputs=[SOGbid],
					)
					ONNX_OP_LIST.append(SOGbn)
					SoG_I.append(SOGbid)

				SOGid = 'SOG_'+str(e)
				SOGn = helper.make_node(
					'Sum',
					inputs=SoG_I,
					outputs=[SOGid],
				)
				ONNX_OP_LIST.append(SOGn)
				
				SOGscaledId = 'SOGscaled_'+str(e)
				SOGscaledn = helper.make_node(
					'Mul',
					inputs=[SOGid,kinvid],
					outputs=[SOGscaledId],
				)
				ONNX_OP_LIST.append(SOGscaledn)
			
				PERTURBWEIGHTSid = 'PERTURBWEIGHTS_'+str(e)
				PERTURBWEIGHTS = helper.make_tensor_value_info(PERTURBWEIGHTSid, DTYPE, shape=(Ys,Yt))
				PERTURBWEIGHTSn = helper.make_node(
					'Add',
					inputs=[WEIGHTSid,SOGscaledId],
					outputs=[PERTURBWEIGHTSid],
				)
				ONNX_OP_LIST.append(PERTURBWEIGHTSn)

				EXPWEIGHTSid = 'EXPWEIGHTS_'+str(s)+'_'+str(t)
				EXPWEIGHTS = helper.make_tensor_value_info(EXPWEIGHTSid, DTYPE, shape=(Ys,Yt))
				EXPWEIGHTSn = helper.make_node(
					'Exp',
					inputs=[PERTURBWEIGHTSid],
					outputs=[EXPWEIGHTSid],
				)
				ONNX_OP_LIST.append(EXPWEIGHTSn)
				
			else:
			
				EXPWEIGHTSid = 'EXPWEIGHTS_'+str(s)+'_'+str(t)
				EXPWEIGHTS = helper.make_tensor_value_info(EXPWEIGHTSid, DTYPE, shape=(Ys,Yt))
				EXPWEIGHTSn = helper.make_node(
					'Exp',
					inputs=[WEIGHTSid],
					outputs=[EXPWEIGHTSid],
				)
				ONNX_OP_LIST.append(EXPWEIGHTSn)
			
			tEXPWEIGHTSid = 'EXPWEIGHTS_'+str(t)+'_'+str(s)
			tEXPWEIGHTS = helper.make_tensor_value_info(tEXPWEIGHTSid, DTYPE, shape=(Yt,Ys))
			tEXPWEIGHTSn = helper.make_node(
				'Transpose',
				inputs=[EXPWEIGHTSid],
				outputs=[tEXPWEIGHTSid],
			)
			ONNX_OP_LIST.append(tEXPWEIGHTSn)

		ONECOLD_VALUESid = 'ONECOLD_VALUES'
		ONECOLD_VALUES = helper.make_tensor_value_info(ONECOLD_VALUESid, ITYPE, shape=(2,))
		ONECOLD_VALUESvals = numpy.array([1,0],dtype=self._Model_incomplete__idxtype)
		ONECOLD_VALUESn = helper.make_node(
			'Constant',
			inputs=[],
			outputs=[ONECOLD_VALUESid],
		 	value=helper.make_tensor(
				name=ONECOLD_VALUESid+'_content',
				data_type=ITYPE,
				dims=ONECOLD_VALUESvals.shape,
				vals=ONECOLD_VALUESvals.flatten(),
			),
		)
		ONNX_OP_LIST.append(ONECOLD_VALUESn)

		ONEHOT_VALUESid = 'ONEHOT_VALUES'
		ONEHOT_VALUES = helper.make_tensor_value_info(ONEHOT_VALUESid, ITYPE, shape=(2,))
		ONEHOT_VALUESvals = numpy.array([0,1],dtype=self._Model_incomplete__idxtype)
		ONEHOT_VALUESn = helper.make_node(
			'Constant',
			inputs=[],
			outputs=[ONEHOT_VALUESid],
		 	value=helper.make_tensor(
				name=ONEHOT_VALUESid+'_content',
				data_type=ITYPE,
				dims=ONEHOT_VALUESvals.shape,
				vals=ONEHOT_VALUESvals.flatten(),
			),
		)
		ONNX_OP_LIST.append(ONEHOT_VALUESn)
			
		for v in range(self.graph.nodes):
			nn = len(Ne[v])

			NNid = 'NN_'+str(v)
			NN = helper.make_tensor_value_info(NNid, ITYPE, shape=(1,1))
			NNval = numpy.array([nn],dtype=self._Model_incomplete__idxtype)
			NNn = helper.make_node(
				'Constant',
				inputs=[],
				outputs=[NNid],
			 	value=helper.make_tensor(
					name=NNid+'_content',
					data_type=ITYPE,
					dims=NNval.shape,
					vals=NNval.flatten(),
				),
			)
			ONNX_OP_LIST.append(NNn)
			
			NUMid = 'NUM_'+str(v)
			NUM = helper.make_tensor_value_info(NUMid, ITYPE, shape=(1,1))
			NUMval = numpy.array([v],dtype=self._Model_incomplete__idxtype)
			NUMn = helper.make_node(
				'Constant',
				inputs=[],
				outputs=[NUMid],
			 	value=helper.make_tensor(
					name=NUMid+'_content',
					data_type=ITYPE,
					dims=NUMval.shape,
					vals=NUMval.flatten(),
				),
			)
			ONNX_OP_LIST.append(NUMn)

			for iw in range(nn):
				w = Ne[v][iw]
				IDXid = 'IDX_'+str(v)+'_'+str(w)
				IDX = helper.make_tensor_value_info(IDXid, ITYPE, shape=(1,))
				IDXval = numpy.array([iw],dtype=self._Model_incomplete__idxtype)
				IDXn = helper.make_node(
					'Constant',
					inputs=[],
					outputs=[IDXid],
				 	value=helper.make_tensor(
						name=IDXid+'_content',
						data_type=ITYPE,
						dims=IDXval.shape,
						vals=IDXval.flatten(),
					),
				)
				ONNX_OP_LIST.append(IDXn)

				FMASKED_NEIGHBORSid = 'FMASKED_NEIGHBORS_'+str(v)+'_'+str(w)
				FMASKED_NEIGHBORS = helper.make_tensor_value_info(FMASKED_NEIGHBORSid, ITYPE, shape=(nn,1))
				FMASKED_NEIGHBORSn = helper.make_node(
					'OneHot',
					inputs=[IDXid, NNid, ONECOLD_VALUESid],
					outputs=[FMASKED_NEIGHBORSid],
					axis=0,
				)
				ONNX_OP_LIST.append(FMASKED_NEIGHBORSn)
				
				MASKED_NEIGHBORSid = 'MASKED_NEIGHBORS_'+str(v)+'_'+str(w)
				MASKED_NEIGHBORS = helper.make_tensor_value_info(FMASKED_NEIGHBORSid, DTYPE, shape=(nn,1))
				MASKED_NEIGHBORSn = helper.make_node(
					'Cast',
					inputs=[FMASKED_NEIGHBORSid],
					outputs=[MASKED_NEIGHBORSid],
					to=DTYPE,
				)
				ONNX_OP_LIST.append(MASKED_NEIGHBORSn)

		NUMid = 'NUM_'+str(self.graph.nodes)
		NUM = helper.make_tensor_value_info(NUMid, ITYPE, shape=(1,1))
		NUMval = numpy.array([self.graph.nodes],dtype=self._Model_incomplete__idxtype)
		NUMn = helper.make_node(
			'Constant',
			inputs=[],
			outputs=[NUMid],
		 	value=helper.make_tensor(
				name=NUMid+'_content',
				data_type=ITYPE,
				dims=NUMval.shape,
				vals=NUMval.flatten(),
			),
		)
		ONNX_OP_LIST.append(NUMn)
		################################################################################
		# INPUT (OBSERVED) VALUES
		################################################################################

		OBSERVED = helper.make_tensor_value_info('observed_data', ITYPE, shape=(self.graph.nodes,))

		################################################################################
		# INITIAL OUTGOING LOG-MESSAGES v -> w, STATE SPACES, AND OBS-VECTORS
		################################################################################

	#		DBG_SLICES = []

		for v in range(self.graph.nodes):
			Yv = int(self.states[v])
			for w in Ne[v]:
				INITIALMSGid = 'LOGMSG_'+str(w)+'_'+str(v)+'_0'
				INITIALMSG = helper.make_tensor_value_info(INITIALMSGid, DTYPE, shape=(Yv,1))
				INITIALMSGval = numpy.zeros(Yv).reshape(Yv,1).astype(self._Model_incomplete__valtype)
				INITIALMSGn = helper.make_node(
					'Constant',
					inputs=[],
					outputs=[INITIALMSGid], # all messages from w to v in iter 0
				 	value=helper.make_tensor(
						name=INITIALMSGid+'_content',
						data_type=DTYPE,
						dims=INITIALMSGval.shape,
						vals=INITIALMSGval.flatten(),
					),
				)
				ONNX_OP_LIST.append(INITIALMSGn)

			XVid = 'XV'+str(v)
			XV  = helper.make_tensor_value_info(XVid, ITYPE, shape=(1,))
			XVv = numpy.array([Yv],dtype=self._Model_incomplete__idxtype)
			XVn = helper.make_node(
				'Constant',
				inputs=[],
				outputs=[XVid],
			 	value=helper.make_tensor(
					name=XVid+'_content',
					data_type=ITYPE,
					dims=XVv.shape,
					vals=XVv.flatten(),
				),
			)
			ONNX_OP_LIST.append(XVn)

			VERTEX_SLICEid = 'OBSERVED_VALUE_'+str(v)
			VERTEX_SLICE = helper.make_tensor_value_info(VERTEX_SLICEid, ITYPE, shape=(Yv,1))
			VERTEX_SLICEn = helper.make_node(
				'Slice',
				inputs=['observed_data','NUM_'+str(v),'NUM_'+str(v+1)],
				outputs=[VERTEX_SLICEid],
			)
			ONNX_OP_LIST.append(VERTEX_SLICEn)
			
			FIS_NOT_OBSERVEDid = 'FIS_NOT_OBSERVED_'+str(v)
			FIS_NOT_OBSERVED = helper.make_tensor_value_info(FIS_NOT_OBSERVEDid, ITYPE, shape=(1,1))
			FIS_NOT_OBSERVEDn = helper.make_node(
				'GreaterOrEqual',
				inputs=[VERTEX_SLICEid,XVid],
				outputs=[FIS_NOT_OBSERVEDid],
			)
			ONNX_OP_LIST.append(FIS_NOT_OBSERVEDn)
			
			IS_NOT_OBSERVEDid = 'IS_NOT_OBSERVED_'+str(v)
			IS_NOT_OBSERVED = helper.make_tensor_value_info(IS_NOT_OBSERVEDid, DTYPE, shape=(1,1))
			IS_NOT_OBSERVEDn = helper.make_node(
				'Cast',
				inputs=[FIS_NOT_OBSERVEDid],
				outputs=[IS_NOT_OBSERVEDid],
				to=DTYPE,
			)
			ONNX_OP_LIST.append(IS_NOT_OBSERVEDn)
			
			FOBSVECid = 'FOBSERVATION_VECTOR_'+str(v)
			FOBSVEC = helper.make_tensor_value_info(FOBSVECid, ITYPE, shape=(Yv,1))
			FOBSVECn = helper.make_node(
				'OneHot',
				inputs=[VERTEX_SLICEid, XVid, ONEHOT_VALUESid],
				outputs=[FOBSVECid],
				axis=0,
			)
			ONNX_OP_LIST.append(FOBSVECn)
			
			tFOBSVECid = 'tFOBSERVATION_VECTOR_'+str(v)
			tFOBSVEC = helper.make_tensor_value_info(tFOBSVECid, ITYPE, shape=(1,Yv))
			tFOBSVECn = helper.make_node(
				'Transpose',
				inputs=[FOBSVECid],
				outputs=[tFOBSVECid],
			)
			ONNX_OP_LIST.append(tFOBSVECn)

			OBSVECid = 'OBSERVATION_VECTOR_'+str(v)
			OBSVEC = helper.make_tensor_value_info(OBSVECid, DTYPE, shape=(1,Yv))
			OBSVECn = helper.make_node(
				'Cast',
				inputs=[tFOBSVECid],
				outputs=[OBSVECid],
				to=DTYPE,
			)
			ONNX_OP_LIST.append(OBSVECn)

		################################################################################
		# Unroll LBP
		################################################################################

		if iterations is None:
			ITERS = self.graph.edges
		else:
			ITERS = iterations

		for I in range(ITERS):
			for v in range(self.graph.nodes):
				Yv = int(self.states[v])
				nn = len(Ne[v])

				# concatenate incoming log-message vector into on large matrix
				IN = ['LOGMSG_'+str(w)+'_'+str(v)+'_'+str(I) for w in Ne[v]]
				
				INCOMINGSid = 'incoming_'+str(v)+'_'+str(I)
				INCOMINGS = helper.make_tensor_value_info(INCOMINGSid, DTYPE, shape=(Yv,nn))
				INCOMINGSn = helper.make_node(
					'Concat',
					inputs=IN,
					outputs=[INCOMINGSid],
					axis=1,
				)
				ONNX_OP_LIST.append(INCOMINGSn)
				
				# messages from v to w
				for iw in range(nn):
					w = Ne[v][iw]
					e = NeE[v][iw]
					Yw = int(self.states[w])

					MSGSUMid = 'MSGSUM_'+str(v)+'_'+str(w)+'_'+str(I) # sum of incoming log-messages not from w
					MSGSUM = helper.make_tensor_value_info(MSGSUMid, DTYPE, shape=(Yv,1))
					MSGSUMn = helper.make_node(
						'MatMul',
						inputs=[INCOMINGSid,'MASKED_NEIGHBORS_'+str(v)+'_'+str(w)],
						outputs=[MSGSUMid],
					)
					ONNX_OP_LIST.append(MSGSUMn)
					
					EXPMSGSUMid = 'EXPMSGSUM_'+str(v)+'_'+str(w)+'_'+str(I)
					EXPMSGSUM = helper.make_tensor_value_info(EXPMSGSUMid, DTYPE, shape=(Yv,1))
					EXPMSGSUMn = helper.make_node(
						'Exp',
						inputs=[MSGSUMid],
						outputs=[EXPMSGSUMid],
					)
					ONNX_OP_LIST.append(EXPMSGSUMn)

					tEXPMSGSUMid = 'tEXPMSGSUM_'+str(v)+'_'+str(w)+'_'+str(I)
					tEXPMSGSUM = helper.make_tensor_value_info(tEXPMSGSUMid, DTYPE, shape=(1,Yv))
					tEXPMSGSUMn = helper.make_node(
						'Transpose',
						inputs=[EXPMSGSUMid],
						outputs=[tEXPMSGSUMid],
					)
					ONNX_OP_LIST.append(tEXPMSGSUMn)
					
					###################################
					# Incorporate Observations
					###################################
					
					StEXPMSGSUMid = 'StEXPMSGSUM_'+str(v)+'_'+str(w)+'_'+str(I)
					StEXPMSGSUM = helper.make_tensor_value_info(StEXPMSGSUMid, DTYPE, shape=(1,Yv))
					StEXPMSGSUMn = helper.make_node(
						'Mul',
						inputs=[tEXPMSGSUMid,'IS_NOT_OBSERVED_'+str(v)],
						outputs=[StEXPMSGSUMid],
					)
					ONNX_OP_LIST.append(StEXPMSGSUMn)

					INOBSVECid = 'INOBS_'+str(v)+'_'+str(w)+'_'+str(I)
					INOBSVEC = helper.make_tensor_value_info(INOBSVECid, DTYPE, shape=(1,Yv))
					INOBSVECn = helper.make_node(
						'Add',
						inputs=[StEXPMSGSUMid,'OBSERVATION_VECTOR_'+str(v)],
						outputs=[INOBSVECid],
					)
					ONNX_OP_LIST.append(INOBSVECn)
					
					###################################
					
					MULMSGid = 'MULMSG_'+str(v)+'_'+str(w)+'_'+str(I)
					MULMSG = helper.make_tensor_value_info(MULMSGid, DTYPE, shape=(Yw,Yv))
					MULMSGn = helper.make_node(
						'Mul',
						inputs=['EXPWEIGHTS_'+str(w)+'_'+str(v),INOBSVECid],
						outputs=[MULMSGid],
					)
					ONNX_OP_LIST.append(MULMSGn)
					
					if probmodel:

						OUTMSGid = 'MSG_'+str(v)+'_'+str(w)+'_'+str(I)
						OUTMSG = helper.make_tensor_value_info(OUTMSGid, DTYPE, shape=(Yw,1))
						OUTMSGn = helper.make_node(
							'ReduceSum',
							inputs=[MULMSGid,CONSTANT_ONEid],
							outputs=[OUTMSGid],
						)
						ONNX_OP_LIST.append(OUTMSGn)
						
					else:
						# The current runtime does not support ReduceMax with DTYPE
						
						OUTMSG1id = 'MSG1_'+str(v)+'_'+str(w)+'_'+str(I)
						OUTMSG1 = helper.make_tensor_value_info(OUTMSG1id, DTYPE, shape=(Yw,Yv))
						OUTMSG1n = helper.make_node(
							'Cast',
							inputs=[MULMSGid],
							outputs=[OUTMSG1id],
							to=TensorProto.FLOAT,
						)
						ONNX_OP_LIST.append(OUTMSG1n)
						
						OUTMSG1bid = 'MSG1b_'+str(v)+'_'+str(w)+'_'+str(I)
						OUTMSG1b = helper.make_tensor_value_info(OUTMSG1bid, DTYPE, shape=(Yw,1))
						OUTMSG1bn = helper.make_node(
							'ReduceMax',
							inputs=[OUTMSG1id],
							outputs=[OUTMSG1bid],
							axes=[1],
						)
						ONNX_OP_LIST.append(OUTMSG1bn)

						OUTMSGid = 'MSG_'+str(v)+'_'+str(w)+'_'+str(I)
						OUTMSG = helper.make_tensor_value_info(OUTMSGid, DTYPE, shape=(Yw,1))
						OUTMSGn = helper.make_node(
							'Cast',
							inputs=[OUTMSG1bid],
							outputs=[OUTMSGid],
							to=DTYPE,
						)
						ONNX_OP_LIST.append(OUTMSGn)
					
					ZOUTMSGid = 'ZMSG_'+str(v)+'_'+str(w)+'_'+str(I)
					ZOUTMSG = helper.make_tensor_value_info(ZOUTMSGid, DTYPE, shape=(1,))
					ZOUTMSGn = helper.make_node(
						'ReduceSum',
						inputs=[OUTMSGid],
						outputs=[ZOUTMSGid],
						keepdims=0,
					)
					ONNX_OP_LIST.append(ZOUTMSGn)

					NORMOUTMSGid = 'NORMMSG_'+str(v)+'_'+str(w)+'_'+str(I)
					NORMOUTMSG = helper.make_tensor_value_info(NORMOUTMSGid, DTYPE, shape=(Yw,1))
					NORMOUTMSGn = helper.make_node(
						'Div',
						inputs=[OUTMSGid,ZOUTMSGid],
						outputs=[NORMOUTMSGid],
					)
					ONNX_OP_LIST.append(NORMOUTMSGn)
					
					FINALOUTMSGid = 'LOGMSG_'+str(v)+'_'+str(w)+'_'+str(I+1)
					FINALOUTMSG = helper.make_tensor_value_info(FINALOUTMSGid, DTYPE, shape=(Yw,1))
					FINALOUTMSGn = helper.make_node(
						'Log',
						inputs=[NORMOUTMSGid],
						outputs=[FINALOUTMSGid],
					)
					ONNX_OP_LIST.append(FINALOUTMSGn)

		################################################################################
		# VERTEX MARGINALS
		################################################################################

		for v in range(self.graph.nodes):
			Yv = int(self.states[v])
			nn = len(Ne[v])

			# concatenate incoming log-message vector into on large matrix
			IN = ['LOGMSG_'+str(w)+'_'+str(v)+'_'+str(ITERS) for w in Ne[v]]
			
			INCOMINGSid = 'incoming_'+str(v)+'_'+str(ITERS)
			INCOMINGS = helper.make_tensor_value_info(INCOMINGSid, DTYPE, shape=(Yv,nn))
			INCOMINGSn = helper.make_node(
				'Concat',
				inputs=IN,
				outputs=[INCOMINGSid],
				axis=1,
			)
			ONNX_OP_LIST.append(INCOMINGSn)
			
			INSUMid = 'sum_incoming_'+str(v)
			INSUM = helper.make_tensor_value_info(INSUMid, DTYPE, shape=(Yv,))
			INSUMn = helper.make_node(
				'ReduceSum',
				inputs=[INCOMINGSid, CONSTANT_ONEid],
				outputs=[INSUMid],
				keepdims=0,
			)
			ONNX_OP_LIST.append(INSUMn)
			
			ExpINSUMid = 'exp_sum_incoming_'+str(v)
			ExpINSUM = helper.make_tensor_value_info(ExpINSUMid, DTYPE, shape=(Yv,))
			ExpINSUMn = helper.make_node(
				'Exp',
				inputs=[INSUMid],
				outputs=[ExpINSUMid],
			)
			ONNX_OP_LIST.append(ExpINSUMn)
			
			###################################
			# Incorporate Observations
			###################################
					
			SINSUMid = 'switched_exp_sum_incoming_'+str(v)
			SINSUM = helper.make_tensor_value_info(SINSUMid, DTYPE, shape=(Yv,))
			SINSUMn = helper.make_node(
				'Mul',
				inputs=[ExpINSUMid,'IS_NOT_OBSERVED_'+str(v)],
				outputs=[SINSUMid],
			)
			ONNX_OP_LIST.append(SINSUMn)

			MSINSUMid = 'masked_switched_exp_sum_incoming_'+str(v)
			MSINSUM = helper.make_tensor_value_info(INOBSVECid, DTYPE, shape=(Yv,))
			MSINSUMn = helper.make_node(
				'Add',
				inputs=[SINSUMid,'OBSERVATION_VECTOR_'+str(v)],
				outputs=[MSINSUMid],
			)
			ONNX_OP_LIST.append(MSINSUMn)
					
			###################################
			
			ZExpINSUMid = 'Zexp_sum_incoming_'+str(v)
			ZExpINSUM = helper.make_tensor_value_info(ZExpINSUMid, DTYPE, shape=(1,))
			ZExpINSUMn = helper.make_node(
				'ReduceSum',
				inputs=[MSINSUMid],
				outputs=[ZExpINSUMid],
				keepdims=0,
			)
			ONNX_OP_LIST.append(ZExpINSUMn)
			
			MARGINALSid = 'marginals_'+str(v)
			MARGINALS = helper.make_tensor_value_info(MARGINALSid, DTYPE, shape=(Yv,))
			MARGINALSn = helper.make_node(
				'Div',
				inputs=[MSINSUMid,ZExpINSUMid],
				outputs=[MARGINALSid],
			)
			ONNX_OP_LIST.append(MARGINALSn)
			
			rsMARGINALSid = 'rs_marginals_'+str(v)
			rsMARGINALS = helper.make_tensor_value_info(rsMARGINALSid, DTYPE, shape=(Yv,))
			rsMARGINALSn = helper.make_node(
				'Reshape',
				inputs=[MARGINALSid,'XV'+str(v)],
				outputs=[rsMARGINALSid],
			)
			ONNX_OP_LIST.append(rsMARGINALSn)
			
			PROBv.append(rsMARGINALSid)
	#			DBG_SLICES.append(MARGINALSid)
			
			AMAXMARGINALSid = 'argmax_marginals_'+str(v)
			AMAXMARGINALS = helper.make_tensor_value_info(AMAXMARGINALSid, ITYPE, shape=(1,))
			AMAXMARGINALSn = helper.make_node(
				'ArgMax',
				inputs=[MARGINALSid],
				outputs=[AMAXMARGINALSid],
				axis=1,
				keepdims=0,
				select_last_index=1,
			)
			ONNX_OP_LIST.append(AMAXMARGINALSn)
			
			MAPv.append(AMAXMARGINALSid)

		################################################################################
		# OUTPUT
		################################################################################

		if probmodel:
			PROBid = 'PROB'
			s = sum(self.states.tolist())
			OUTPUT = helper.make_tensor_value_info(PROBid, DTYPE, shape=(int(s),))
			PROBn = helper.make_node(
				'Concat',
				inputs=PROBv,
				outputs=[PROBid],
				axis=0,
			)
			ONNX_OP_LIST.append(PROBn)

		else:
			MAPid = 'MAP'
			OUTPUT = helper.make_tensor_value_info(MAPid, ITYPE, shape=(self.graph.nodes,))
			MAPn = helper.make_node(
				'Concat',
				inputs=MAPv,
				outputs=[MAPid],
				axis=0,
			)
			ONNX_OP_LIST.append(MAPn)
			
	#		DBGid = 'DBG'
	#		DBG = helper.make_tensor_value_info(DBGid, DTYPE, shape=(8,3))
	#		DBGn = helper.make_node(
	#			'Concat',
	#			inputs=DBG_SLICES,
	#			outputs=[DBGid],
	#			axis=0,
	#		)
	#		ONNX_OP_LIST.append(DBGn)

		#OTHER_OUTPUT = helper.make_tensor_value_info('GAMMA_SAMPLE_0_s0', DTYPE, shape=(2,2,))

		graph_def = helper.make_graph(
			ONNX_OP_LIST,
			'unrolled_pxpy_model',
			[OBSERVED],
			[OUTPUT]
		)

		info = {
			"n": self.graph.nodes,
			"N": self.num_instances,
			"LL": self.LL,
			"Y": self.states.tolist()
		}

		onnx_model = helper.make_model(graph_def, producer_name='pxpy', producer_version=str(self.swversion), model_version=1, doc_string=json.dumps(info))
		onnx.save(onnx_model, fname)
		

	def export_onnx_marginal_inference(self,filename,iterations=None):
		self.export_onnx(filename,True,False,iterations)

	def export_onnx_MAP_inference(self,filename,iterations=None):
		self.export_onnx(filename,False,False,iterations)

	def export_onnx_PAM_sampler(self,filename,iterations=None):
		self.export_onnx(filename,False,True,iterations)

