from typing import Iterable, Optional, Union
from memarray import MemristorArray
# from simbrain.power import Power
import json
import pickle
import torch

class Mapping(torch.nn.Module):
    # language=rst
    """
    Abstract base class for mapping neural networks to memristor arrays.
    """

    def __init__(
        self,
        mem_device: dict = {},
        shape: Optional[Iterable[int]] = None,
        **kwargs,
    ) -> None:
        # language=rst
        """
        Abstract base class constructor.
        :param mem_device: Memristor device to be used in learning.
        :param shape: The dimensionality of the layer.
        """
        super().__init__()

        self.device_name = mem_device['device_name'] 
        self.device_structure = mem_device['device_structure']

        if self.device_structure == 'trace':
            self.shape = [1, 1]  # Shape of the memristor crossbar
            for element in shape:
                self.shape[1] *= element
            self.shape = tuple(self.shape)
        elif self.device_structure in {'crossbar', 'mimo'}:
            self.shape = shape
        else:
            raise Exception("Only trace and crossbar architecture are supported!")
        
        self.register_buffer("mem_v", torch.Tensor())
        self.register_buffer("mem_v_read", torch.Tensor())
        self.register_buffer("mem_t", torch.Tensor())
        self.register_buffer("mem_x_read", torch.Tensor())
        self.register_buffer("x", torch.Tensor())
        self.register_buffer("s", torch.Tensor())
        self.register_buffer("readEnergy", torch.Tensor())
        self.register_buffer("writeEnergy", torch.Tensor())

        with open('memristor_data/memristor_device_info.json', 'r') as f:
            self.memristor_info_dict = json.load(f)
        assert self.device_name in self.memristor_info_dict.keys(), "Invalid Memristor Device!"  
        self.vneg = self.memristor_info_dict[self.device_name]['vinput_neg']
        self.vpos = self.memristor_info_dict[self.device_name]['vinput_pos']
        self.Gon = self.memristor_info_dict[self.device_name]['G_on']
        self.Goff = self.memristor_info_dict[self.device_name]['G_off']
        self.dt = self.memristor_info_dict[self.device_name]['delta_t']
        
        self.trans_ratio = 1 / (self.Goff - self.Gon)
        
        self.mem_array = MemristorArray(mem_device=mem_device, shape=self.shape, memristor_info_dict=self.memristor_info_dict)

        self.batch_size = None

        # self.power = Power(mem_device=mem_device, shape=self.shape, memristor_info_dict=self.memristor_info_dict)


    def set_batch_size(self, batch_size) -> None:
        # language=rst
        """
        Sets mini-batch size. Called when memristor is used to mapping traces.
    
        :param batch_size: Mini-batch size.
        """
        self.batch_size = batch_size
        
        self.mem_v = torch.zeros(batch_size, *self.shape, device=self.mem_v.device)
        self.mem_v_read = torch.zeros(batch_size, self.shape[0], device=self.mem_v.device)
        self.mem_t = torch.zeros(batch_size, *self.shape, device=self.mem_t.device)
        self.mem_x_read = torch.zeros(batch_size, self.shape[1], device=self.mem_v.device)
        self.x = torch.zeros(batch_size, *self.shape, device=self.x.device)
        self.s = torch.zeros(batch_size, *self.shape, device=self.s.device)
        self.readEnergy = torch.zeros(batch_size, *self.shape, device=self.readEnergy.device)
        self.writeEnergy = torch.zeros(batch_size, *self.shape, device=self.writeEnergy.device)

        self.mem_array.set_batch_size(batch_size=self.batch_size)
        # self.power.set_batch_size(batch_size=self.batch_size)


    def mem_t_calculate(self, mem_step):
        # Calculate the mem_t
        self.mem_t[:, :, :] = mem_step.view(-1, 1)
        self.mem_t *= self.dt 
        
        
    def reset_memristor_variables(self,mem_step) -> None:
        # language=rst
        """
        Abstract base class method for resetting state variables.
        """
        self.mem_v.fill_(-self.vpos)
        self.mem_t_calculate(mem_step=mem_step)        
        # Adopt large negative pulses to reset the memristor array
        self.mem_array.memristor_write(mem_v=self.mem_v, mem_t=self.mem_t)

        
    def update_SAF_mask(self) -> None:
        self.mem_array.update_SAF_mask()


    # def mapping_write(self, s, mem_step):
    #     if self.device_structure == 'trace':
    #         if s.dim() == 4:
    #             self.s = s.flatten(2, 3)
    #         elif s.dim() == 2:
    #             self.s = torch.unsqueeze(s, 1)
        
    #     # nn to mem
    #     self.mem_v = self.s.float()
    #     self.mem_v[self.mem_v == 0] = self.vneg
    #     self.mem_v[self.mem_v == 1] = self.vpos   
    #     self.mem_t_calculate(mem_step=mem_step)      

    #     mem_c = self.mem_array.memristor_write(mem_v=self.mem_v, mem_t=self.mem_t)
        
    #     # mem to nn
    #     self.x = (mem_c - self.Gon) * self.trans_ratio

    #     if self.device_structure == 'trace':
    #         if s.dim() == 4:
    #             self.x = self.x.reshape(s.size(0), s.size(1), s.size(2), s.size(3))
    #         elif s.dim() == 2:
    #             self.x = self.x.squeeze()

    #     return self.x

    # def mapping_read(self, s):
    #     if self.device_structure == 'trace':
    #         if s.dim() == 4:
    #             s = s.flatten(2, 3)
    #         elif s.dim() == 2:
    #             s = torch.unsqueeze(s, 1)

    #     # Read Voltage generation
    #     v_read = 0.01 # TODO: make v_read a parameter in memristor_device_info.json like vneg/vpos
    #     # For every batch, read is not necesary when there is no spike s
    #     s_sum = torch.sum(s, dim=2).squeeze()

    #     self.mem_v_read.zero_()
    #     self.mem_v_read[s_sum.bool()] = v_read

    #     mem_i = self.mem_array.memristor_read(mem_v=self.mem_v_read)

    #     # current to trace
    #     self.mem_x_read = (mem_i/v_read - self.Gon) * self.trans_ratio

    #     self.mem_x_read[~s_sum.bool()] = 0

    #     if self.device_structure == 'trace':
    #         if s.dim() == 4:
    #             self.mem_x_read = self.mem_x_read.reshape(s.size(0), s.size(1), s.size(2), s.size(3))
    #         elif s.dim() == 2:
    #             self.mem_x_read = self.mem_x_read.squeeze()

    #     return self.mem_x_read

class MimoMapping(Mapping):
    # language=rst
    """
    Mapping MIMO to memristor arrays.
    """

    def __init__(
        self,
        mem_device: dict = {},
        shape: Optional[Iterable[int]] = None,
        **kwargs,
    ) -> None:
        # language=rst
        """
        Abstract base class constructor.
        :param mem_device: Memristor device to be used in learning.
        :param shape: The dimensionality of the memristor array.
        """
        super().__init__(
            mem_device=mem_device,
            shape=shape
        )

        self.register_buffer("write_pulse_no", torch.Tensor())
        self.write_pulse_no = torch.zeros(*self.shape, device=self.mem_v.device)

        with open('memristor_data/memristor_lut.pkl', 'rb') as f:
            self.memristor_luts = pickle.load(f)
        assert self.device_name in self.memristor_luts.keys(), "No Look-Up-Table Data Available for the Target Memristor Type!"  
    
        self.set_batch_size(1)
        self.mem_t_calculate(mem_step=torch.tensor([0])) 
        

    def mapping_write(self, target_x):
        # Memristor reset first
        self.mem_v.fill_(-100) #TODO: check the reset voltage
        # Adopt large negative pulses to reset the memristor array
        self.mem_array.memristor_write(mem_v=self.mem_v)

        # Vector to Pulse Serial
        self.write_pulse_no = self.m2v(target_x)
        total_wr_cycle = self.memristor_luts[self.device_name]['total_no']
        write_voltage = self.memristor_luts[self.device_name]['voltage']

        # Matrix to memristor
        counter = torch.ones_like(self.mem_v)
        # Memristor programming using multiple identical pulses (up to 400)
        for t in range(total_wr_cycle):
            self.mem_v = ((counter * t) < self.write_pulse_no) * write_voltage
            self.mem_array.memristor_write(mem_v=self.mem_v)


    def m2v(self, target_matrix):
        # Target_matrix ranging [0, 1]
        within_range = (target_matrix >= 0) & (target_matrix <= 1)
        assert torch.all(within_range), "The target Matrix Must be in the Range [0, 1]!"  

        # Target x to target conductance
        target_c = target_matrix / self.trans_ratio + self.Gon

        # Get access to the look-up-table of the target memristor
        luts = self.memristor_luts[self.device_name]['conductance']

        # Find the nearest conductance value
        c_diff = torch.abs(torch.tensor(luts) - target_c.unsqueeze(2))
        nearest_pulse_no = torch.argmin(c_diff, dim=2)

        return nearest_pulse_no



