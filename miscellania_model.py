import math
import matplotlib.pyplot as plt
import numpy as np

class Kingdom:
  '''
  A model of the Kingdom of Miscellania in Old School Runescape.
  '''
  def __init__(self, starting_cash, base_revenue, completed_royal_trouble=True, starting_approval=1.0):
    '''
    starting_cash: How much money starts in the coffer
    base_revenue: Revenue to be gained in 1 day, assuming maximum approval
                  and >= 750k in the coffers
    completed_royal_trouble: Whether or not the Royal Trouble quest has been completed
    starting_approval: Starting approval rate (between 0.0 and 1.0)
    '''
    self.approval_ = max(0.0, min(1.0, starting_approval))
    self.coffer_ = round(starting_cash)
    self.starting_cash_ = round(starting_cash)
    self.base_revenue_ = round(base_revenue)
    self.decay_rate_ = 0.01 if completed_royal_trouble else 0.025
    self.max_payroll_ = 75000 if completed_royal_trouble else 50000
    self.revenue_ = 0

  def injectCash(self, cash):
    '''Add money to the treasury'''
    self.coffer_ += round(cash)

  def getPayroll(self):
    '''Calculate the payroll for 1 day'''
    return math.ceil(min(self.coffer_ * 0.10, self.max_payroll_))

  def decayApproval(self):
    '''Reduce approval rating according to decay rate'''
    if self.approval_ <= 0.25:
      return
    self.approval_ = round(max(0.25, self.approval_ - self.decay_rate_), 2)

  def advanceDay(self):
    '''Calculate revenue, change in treasury value, and change in approval for 1 day'''
    payroll = self.getPayroll()
    if payroll <= self.coffer_:
      gains = round(self.base_revenue_ * self.approval_ * payroll / self.max_payroll_)
      self.coffer_ -= payroll
      self.revenue_ += gains
    self.decayApproval()

  def spendAllMoney(self, verbose=False):
    '''
    Continue to advance days until the coffers are empty
    
    verbose: Print information along the way
    '''
    day=0
    while self.coffer_ > 0:
      if verbose:
        print("Day: {}, Coffers: {:,}, Approval: {:.2f}%".format(day, self.coffer_, self.approval_*100))
      self.advanceDay()
      day += 1
    profit = self.revenue_ - self.starting_cash_
    if verbose:
      print("Ran out of money on day {}, after earning {:,}".format(day, self.revenue_))
      print("Total profit: {:,}".format(profit))
    return profit, day

if __name__ == "__main__":
  starting_cash_values = [10000*i for i in range(1001)]
  profits = []
  days = []
  assumed_base_revenue = 125000
  for cash in starting_cash_values:
    kingdom = Kingdom(cash, assumed_base_revenue)
    profit, day = kingdom.spendAllMoney(verbose=False)
    profits.append(profit)
    days.append(day)

  # Get highest profit value
  index = profits.index(max(profits))
  best_starting_cash = starting_cash_values[index]
  day = days[index]

  #############
  # Plot things
  #############

  # Grid and axis settings
  plt.grid(color='grey', linestyle='--',linewidth=0.5)
  plt.xlabel("Starting cash", fontsize=15)
  plt.ylabel("Profits", fontsize=15)
  plt.ticklabel_format(style='plain', axis='both')
  
  x_tick_values = np.linspace(min(starting_cash_values), max(starting_cash_values), num=6)
  x_tick_labels = ['{:,.0f}'.format(value) for value in x_tick_values]

  y_tick_values = np.linspace(min(profits), max(profits), num=6)
  y_tick_labels = ['{:,.0f}'.format(value) for value in y_tick_values]

  plt.xticks(x_tick_values, x_tick_labels )
  plt.yticks(y_tick_values, y_tick_labels )

  plt.title("Profits vs. Starting Cash", fontsize=20)

  # Plot things
  plt.plot(starting_cash_values, profits, label='Base revenue = {}'.format(assumed_base_revenue))
  plt.axvline(x=best_starting_cash, color='red')
  plt.axhline(y=0, color='black')
  label = "{:,} staring cash will\ngenerate {:,} in profits\nafter {} days".format(best_starting_cash, max(profits), day)
  plt.annotate(label, # this is the text
                 (best_starting_cash,min(profits)), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(10,0), # distance from text to points (x,y)
                 ha='left') # horizontal alignment can be left, right or center
  plt.annotate('0 profit', # this is the text
                 (x_tick_values[-2], 0), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(0,-10), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center
  plt.legend(loc='upper right')
  plt.tight_layout()
  plt.show()

