import time
import random

class VehicleDataSimulator:
    """Simulates realistic vehicle data with natural variations."""
    
    def __init__(self):
        # initialize values
        self.speed = 0
        self.rpm = 0
        self.current = 0
        self.eng_temp = 20
        
        # what the values will update/trend towards within the next cycle
        self.target_speed = 0
        self.target_rpm = 0
        self.target_current = 0
        
        # movement state
        self.accelerating = False
        self.last_update = time.time()
        
        # to start a cycle of simulation
        self._update_targets()
    
    def _update_targets(self):
        """Periodically change target values to simulate driving patterns."""
        # randomly decide to accelerate, maintain speed, decelerate, or idle. although the weights may not be realistic, it shouldn't matter too much
        driving_state = random.choices(
            ['accelerate', 'maintain', 'decelerate', 'idle'],
            weights=[0.3, 0.4, 0.2, 0.1]
        )[0]
        
        if driving_state == 'accelerate':
            self.accelerating = True
            self.target_speed = min(140, self.speed + random.uniform(10, 30))
            self.target_rpm = min(6000, self.rpm + random.uniform(500, 1500))
            self.target_current = min(10, self.current + random.uniform(1, 3))
        elif driving_state == 'maintain':
            self.accelerating = True
            # have the values fluctuate slightly
            self.target_speed = max(0, min(140, self.speed + random.uniform(-5, 5)))
            self.target_rpm = max(0, min(6000, self.rpm + random.uniform(-200, 200)))
            self.target_current = max(0, min(10, self.current + random.uniform(-0.5, 0.5)))
        elif driving_state == 'decelerate':
            self.accelerating = False
            self.target_speed = max(0, self.speed - random.uniform(10, 25))
            self.target_rpm = max(0, self.rpm - random.uniform(500, 1200))
            self.target_current = max(0, self.current - random.uniform(1, 2.5))
        else:  # idle
            self.accelerating = False
            self.target_speed = 0
            self.target_rpm = random.uniform(800, 1000)  # "normal" idle RPM
            self.target_current = random.uniform(0.1, 0.5)  # low current
        
        # Ensure that target_rpm and target_speed have a consistent relationship
        if self.target_speed > 0 and self.target_rpm < 1200:
            # If moving, RPM should be higher than idle
            self.target_rpm = 1200 + (self.target_speed * 20)
        elif self.target_speed == 0 and self.target_rpm > 1000:
            # If stopped, RPM should be at idle level or 0
            self.target_rpm = random.uniform(800, 1000)
        
    def update(self):
        """Update all vehicle parameters based on time and targets."""
        current_time = time.time()
        elapsed = current_time - self.last_update
        self.last_update = current_time
        
        # smoothly move current values toward target values
        speed_rate = 15 * elapsed  # Units per second
        rpm_rate = 400 * elapsed
        current_rate = 2 * elapsed
        
        # Update speed with some randomness
        if abs(self.speed - self.target_speed) > 0.5:
            direction = 1 if self.target_speed > self.speed else -1
            self.speed += direction * min(speed_rate, abs(self.target_speed - self.speed))
            # Add minor fluctuations
            self.speed += random.uniform(-0.5, 0.5)
            self.speed = max(0, self.speed)  # Can't go below 0
        
        # Update RPM with relationship to speed and some randomness
        if abs(self.rpm - self.target_rpm) > 20:
            direction = 1 if self.target_rpm > self.rpm else -1
            self.rpm += direction * min(rpm_rate, abs(self.target_rpm - self.rpm))
            # Add minor fluctuations
            self.rpm += random.uniform(-30, 30)
            self.rpm = max(0, self.rpm)  # Can't go below 0
        
        # Enforce realistic relationship between speed and RPM
        # If vehicle is stopped, RPM should be at idle or 0
        if self.speed < 0.5:  # Effectively zero speed
            if self.rpm > 1100:  # Above idle
                self.rpm = random.uniform(800, 1000)  # Set to idle
        # If RPM is above idle, vehicle must be moving
        elif self.rpm > 1100 and self.speed < 1.0:
            self.speed = max(1.0, self.rpm / 1000)  # Ensure minimal movement
        
        # Update current based on acceleration state
        if abs(self.current - self.target_current) > 0.1:
            direction = 1 if self.target_current > self.current else -1
            self.current += direction * min(current_rate, abs(self.target_current - self.current))
            # Add minor fluctuations
            self.current += random.uniform(-0.2, 0.2)
            self.current = max(0, self.current)  # Can't go below 0
        
        # Engine temperature logic - slowly rises when RPM is high, slowly falls when low
        temp_change = 0
        if self.rpm > 3000:
            # Temperature rises faster at high RPM
            temp_change = 2 * elapsed
        elif self.rpm > 1500:
            # Moderate temperature rise
            temp_change = 0.5 * elapsed
        elif self.rpm < 1000 and self.eng_temp > 40:
            # Cool down when idle and above ambient
            temp_change = -0.3 * elapsed
        
        # Add randomness to temperature
        temp_change += random.uniform(-0.1, 0.1)
        self.eng_temp = min(110, max(20, self.eng_temp + temp_change))
        
        # Occasionally update target values
        if random.random() < 0.20:  # 20% chance per update
            self._update_targets()

# use a singleton
_simulator = VehicleDataSimulator()

def get_speed():
    """Retrieve simulated speed."""
    _simulator.update()
    return round(_simulator.speed)

# We don't need to call update() in the rest as it's already called in get_speed()
def get_rpm():
    """Retrieve simulated RPM."""
    return round(_simulator.rpm)

def get_current():
    """Retrieve simulated current usage."""
    return _simulator.current

def get_eng_temp():
    """Retrieve simulated engine temperature."""
    return _simulator.eng_temp
