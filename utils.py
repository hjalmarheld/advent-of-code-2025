import heapq


def read_input(
        path: str,
        listify: bool=False,
        arrayify: bool=False,
        matrixify: bool=False):

    with open(path) as file:
        data = file.read()

    if arrayify:
        data = [list(i) for i in data.splitlines()]
    elif matrixify:
        data = Matrix([list(i) for i in data.splitlines()])
    elif listify:
        data = data.splitlines()

    return data


class matrix:
    """
    utility class for matrix methods
    """
    @staticmethod
    def get_locs(
            M:list[list],
            s:...
        ) -> list[tuple]:
        "find all locations of s"
        locs = []
        for x, row in enumerate(M):
            for y, char in enumerate(row):
                if char==s:
                    locs.append((x, y))
        return locs

    @staticmethod
    def unique(
            M:list[list],
        ) -> set:
        return set(sum(M, []))

    @staticmethod
    def replace(
            M:list[list],
            s1=...,
            s2=...
        ) -> list[list]:
        for x, y in matrix.get_locs(M, s1):
            M[x][y] = s2
        return M


    @staticmethod
    def transpose(
            M:list[list]
        ) -> list[list]:
        """
        transpose a list of list matrix
        """
        return list(map(list, zip(*M)))
    
    @staticmethod
    def turn(
            M:list[list]
        ) -> list[list]:
        """
        turn list of lists 90 deg clockwise
        """
        return list(map(list,(zip(*reversed(M)))))
    
    @staticmethod
    def count(
            M:list[list],
            s:...
        ) -> int:
        """
        return count of specific item in matrix
        """
        return len(matrix.get_locs(M, s))
    

    @staticmethod
    def get_neighbors(
            M:list[list],
            loc:tuple[int],
            diag:bool=False,
            direction:bool=False
        ):
        """
        get loc of neighbouring cells
        """
        # check point inside cell
        assert 0<=loc[0]<len(M) and 0<=loc[1]<len(M[1])
        neighbors = []
        # add horizontal and vertical neighbours
        x = [1, 0, -1, 0]
        y = [0, 1, 0, -1]
        dirs = ['D', 'R', 'U', 'L']
        for i in range(4):
            x_ = loc[0] + x[i]
            y_ = loc[1] + y[i]
            dir_ = dirs[i]
            if 0<=x_<len(M) and 0<=y_<len(M[1]):
                if not direction:
                    neighbors.append((x_, y_))
                else:
                    neighbors.append((x_, y_, dir_))
        # add diagonal neighbors
        if diag:
            x = [1, 1, -1, -1]
            y = [1, -1, 1, -1]
            for i in range(4):
                x_ = loc[0] + x[i]
                y_ = loc[1] + y[i]
                if 0<=x_<len(M) and 0<=y_<len(M[1]):
                    neighbors.append((x_, y_))
        return neighbors
    
    
    @staticmethod
    def floodfill(
            M:list[list],
            loc:tuple[int],
            border:...=1,
            diag:bool=False
        ):
        """
        flood fill algo for list of lists matrix
        """
        assert M[loc[0]][loc[1]]!=border
        queue = set([loc])
        while queue:
            loc = queue.pop()
            M[loc[0]][loc[1]] = border
            neighbors = matrix.get_neighbors(M, loc, diag=diag)
            for neighbor in neighbors:
                if M[neighbor[0]][neighbor[1]] != border:
                    queue.add(neighbor)
        return M


class Matrix(list):
    """
    proper matrix class with some multiindex support
    """
    def __init__(self, M:list[list]):
        self.M = M
        self.index = -1
        self.shape = (len(M), len(M[0]))

    def __getitem__(self, loc):
        """
        multiindexing to get items
        """
        assert isinstance(loc, (tuple, int, float))
        if type(loc)==tuple:
            return self.M[loc[0]][loc[1]]
        else:
            return self.M[int(loc)]
    
    def __setitem__(self, loc, item):
        """
        multiindexing to get items
        """
        assert isinstance(loc, (tuple, int, float))
        if type(loc)==tuple:
            self.M[loc[0]][loc[1]] = item
        else:
            self.M[int(loc)] = item
    
    def __iter__(self):
        yield from self.M
    
    def __str__(self):
        m = f'{len(self.M)}x{len(self.M[0])} matrix: \n'
        m += '\n'.join([''.join([str(i) for i in m]) for m in self.M])
        return m
    
    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return len(self.M)
    
    def __add__(self, s:...):
        return Matrix([[item+s for item in row] for row in self.M])
    
    def __mul__(self, s:...):
        return Matrix([[item*s for item in row] for row in self.M])
    
    def __sub__(self, s:...):
        return Matrix([[item*s for item in row] for row in self.M])
    
    def __pow__(self, s:...):
        return Matrix([[item**s for item in row] for row in self.M])

    def get_locs(self, s:...):
        return matrix.get_locs(self.M, s)
    
    def unique(self):
        return matrix.unique(self.M)
    
    def count(self, s:...):
        return matrix.count(self.M, s)
    
    def get_neighbors(self, loc:tuple[int], diag:bool=False, direction:bool=False):
        return matrix.get_neighbors(self.M, loc, diag, direction)

    def replace(self, s1:..., s2:...):
        return Matrix(matrix.replace(self.M, s1, s2))
    
    def transpose(self):
        return Matrix(matrix.transpose(self.M))
    
    def turn(self):
        return Matrix(matrix.turn(self.M))
    
    def floodfill(self, loc:tuple[int], border:..., diag:bool=False):
        return Matrix(matrix.floodfill(self.M, loc, border, diag))
    
sample_matrix = Matrix([[1,1,1,1], [2,2,2,2], [3,3,3,3]])


def dijkstra(graph, start, end):
    # Initialize distances to all nodes as infinity
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        if current_node == end:
            break
        for neighbor in graph[current_node]:
            distance = current_distance + 1
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    # Reconstruct the shortest path
    shortest_path = []
    node = end
    while node != start:
        shortest_path.append(node)
        for neighbor in graph[node]:
            if distances[node] == distances[neighbor] + 1:
                node = neighbor
                break
    shortest_path.append(start)
    shortest_path.reverse()
    return shortest_path if distances[end] != float('inf') else None

class LMEForwardCurveBuilder:
    
    def build_curve(market_data, spread_data, previous_valuations, config):
        """
        INPUTS:
            market_data: dict/DataFrame with outright prices for each prompt
            spread_data: dict/DataFrame with spread prices between prompts
            previous_valuations: dict/DataFrame with yesterday's curve
            config: dict with configuration parameters
            
        OUTPUTS:
            forward_curve: dict {prompt_date: price} for all dates
            metadata: dict with quality metrics and diagnostics
        """
        
        # STEP 1: Data Preprocessing and Quality Scoring
        # Calculate quality score for each price observation
        processed_outrights = {}
        for prompt, data in market_data.items():
            # Quality components
            ba_quality = 1.0 / (1.0 + (data['ask'] - data['bid']) / data['mid'])
            vol_quality = log(1 + data['volume']) / log(1 + max_volume)
            rec_quality = exp(-hours_since_trade / config['time_decay_halflife'])
            
            # Overall quality (weighted average)
            quality = (config['bid_ask_weight'] * ba_quality +
                      config['volume_weight'] * vol_quality +
                      config['recency_weight'] * rec_quality)
            
            # Reference price (prefer trade > mid > previous)
            if data['last_trade']:
                reference = data['last_trade']
            elif data['mid']:
                reference = data['mid']
            else:
                reference = previous_valuations[prompt]['previous_price']
            
            processed_outrights[prompt] = {
                'reference_price': reference,
                'quality': quality,
                'bid': data['bid'],
                'ask': data['ask']
            }
        
        # Similar processing for spreads...
        processed_spreads = preprocess_spreads(spread_data)
        
        # STEP 2: Establish Anchor Contract (3M)
        # The 3M contract is most liquid and acts as anchor
        anchor_date = get_3m_prompt_date()
        anchor_price = processed_outrights[anchor_date]['reference_price']
        anchor_bounds = (processed_outrights[anchor_date]['bid'],
                        processed_outrights[anchor_date]['ask'])
        
        # STEP 3: Build Initial Curve from Spreads
        # Use graph traversal through spread network
        curve = {anchor_date: anchor_price}
        priced_dates = {anchor_date}
        
        # Iteratively price prompts using spreads from already-priced dates
        while len(priced_dates) < len(market_data):
            for prompt in market_data.keys():
                if prompt in priced_dates:
                    continue
                
                # Find all spreads connecting this prompt to priced dates
                implied_prices = []
                for spread in processed_spreads:
                    if spread['near'] in priced_dates and spread['far'] == prompt:
                        # far = near + spread
                        implied = curve[spread['near']] + spread['reference_spread']
                        implied_prices.append((implied, spread['quality']))
                    elif spread['far'] in priced_dates and spread['near'] == prompt:
                        # near = far - spread
                        implied = curve[spread['far']] - spread['reference_spread']
                        implied_prices.append((implied, spread['quality']))
                
                if implied_prices:
                    # Weighted average of implied prices
                    total_weight = sum(w for _, w in implied_prices)
                    curve[prompt] = sum(p * w for p, w in implied_prices) / total_weight
                    priced_dates.add(prompt)
        
        # STEP 4: Identify Overlapping Spreads
        # Example: Dec25-3M overlaps with Dec25-Jan26 and Jan26-3M
        overlapping_constraints = []
        
        # For Dec25-3M spread
        if exists_spread('Dec25', '3M') and exists_spread('Dec25', 'Jan26') and exists_spread('Jan26', '3M'):
            # Constraint: Spread(Dec25, 3M) = Spread(Dec25, Jan26) + Spread(Jan26, 3M)
            overlapping_constraints.append({
                'direct_spread': ('Dec25', '3M'),
                'component_spreads': [('Dec25', 'Jan26'), ('Jan26', '3M')]
            })
        
        # Repeat for all overlapping combinations...
        
        # STEP 5: Constrained Optimization
        # Minimize: weighted deviations from observations
        # Subject to: arbitrage-free constraints
        
        from scipy.optimize import minimize
        
        prompt_dates = sorted(curve.keys())
        n = len(prompt_dates)
        date_to_idx = {date: i for i, date in enumerate(prompt_dates)}
        
        # Initial guess
        x0 = array([curve[date] for date in prompt_dates])
        
        # Objective function
        def objective(x):
            loss = 0
            
            # Outright price deviations
            for i, date in enumerate(prompt_dates):
                ref = processed_outrights[date]['reference_price']
                quality = processed_outrights[date]['quality']
                loss += quality * (x[i] - ref)**2
            
            # Spread deviations
            for spread in processed_spreads:
                near_idx = date_to_idx[spread['near']]
                far_idx = date_to_idx[spread['far']]
                implied_spread = x[far_idx] - x[near_idx]
                ref_spread = spread['reference_spread']
                quality = spread['quality']
                loss += quality * (implied_spread - ref_spread)**2
            
            # Smoothness penalty (optional)
            for i in range(1, n-1):
                second_deriv = x[i+1] - 2*x[i] + x[i-1]
                loss += config['smoothness_penalty'] * second_deriv**2
            
            return loss
        
        # Constraints
        constraints = []
        
        # Anchor constraint: x[3M] = anchor_price
        anchor_idx = date_to_idx[anchor_date]
        constraints.append({
            'type': 'eq',
            'fun': lambda x: x[anchor_idx] - anchor_price
        })
        
        # Arbitrage-free constraints for overlapping spreads
        for overlap in overlapping_constraints:
            direct_near, direct_far = overlap['direct_spread']
            components = overlap['component_spreads']
            
            # Direct spread = sum of component spreads ± tolerance
            def arbitrage_constraint(x):
                direct = x[date_to_idx[direct_far]] - x[date_to_idx[direct_near]]
                synthetic = sum(x[date_to_idx[f]] - x[date_to_idx[n]] 
                               for n, f in components)
                return direct - synthetic  # Should be ~ 0
            
            constraints.append({
                'type': 'eq',
                'fun': arbitrage_constraint
            })
        
        # Bounds (bid-ask constraints)
        bounds = [(processed_outrights[date]['bid'], 
                   processed_outrights[date]['ask']) 
                  for date in prompt_dates]
        
        # Solve optimization
        result = minimize(
            objective,
            x0,
            method=config['optimization_method'],
            constraints=constraints,
            bounds=bounds,
            options={'maxiter': 1000, 'ftol': 1e-9}
        )
        
        if not result.success:
            # Handle optimization failure
            # Fallback: use initial curve or relax constraints
            pass
        
        optimized_curve = {date: result.x[i] for i, date in enumerate(prompt_dates)}
        
        # STEP 6: Validation
        validation_report = validate_curve(optimized_curve, market_data, spread_data, 
                                          overlapping_constraints, config['arbitrage_tolerance'])
        
        # STEP 7: Interpolation for Full Daily Curve
        # Use monotonic cubic spline for missing dates
        from scipy.interpolate import PchipInterpolator
        complete_curve = interpolate_daily(optimized_curve)
        
        # OUTPUT
        metadata = {
            'timestamp': datetime.now(),
            'anchor_price': anchor_price,
            'num_prompts': len(optimized_curve),
            'optimization_status': result.success,
            'arbitrage_violations': validation_report['arbitrage_violations'],
            'max_deviation': validation_report['max_deviation']
        }
        
        return complete_curve, metadata


# INPUT 1: Market Data for Outright Contracts
MARKET_DATA = {
    'prompt_date': datetime,           # Settlement date
    'bid': float,                      # Bid price ($/tonne)
    'ask': float,                      # Ask price ($/tonne)
    'mid': float,                      # (bid + ask) / 2
    'last_trade': float,               # Last traded price
    'trade_volume': float,             # Volume in lots
    'num_trades': int,                 # Number of trades
    'timestamp': datetime,             # Time of last update
    'contract_type': str               # 'cash', '3M', 'daily', 'weekly', 'monthly'
}

# INPUT 2: Spread (Carry) Data
SPREAD_DATA = {
    'near_leg': datetime,              # Near prompt date
    'far_leg': datetime,               # Far prompt date
    'spread_bid': float,               # Bid for spread (far - near)
    'spread_ask': float,               # Ask for spread
    'spread_mid': float,               # Mid spread
    'spread_last_trade': float,        # Last traded spread
    'spread_volume': float,            # Volume traded
    'spread_num_trades': int,          # Number of trades
    'timestamp': datetime
}

# INPUT 3: Previous Valuations (for continuity)
PREVIOUS_VALUATIONS = {
    'prompt_date': datetime,
    'previous_price': float,           # Yesterday's valuation
    'previous_timestamp': datetime
}

# INPUT 4: Configuration
CONFIG = {
    'anchor_contract': '3M',
    'bid_ask_weight': 0.4,            # Weight for bid-ask quality
    'volume_weight': 0.3,             # Weight for volume quality
    'recency_weight': 0.3,            # Weight for recency quality
    'time_decay_halflife': 2.0,       # Hours for exponential decay
    'arbitrage_tolerance': 0.01,      # $/tonne tolerance
    'smoothness_penalty': 0.05,       # Optional smoothness weight
    'optimization_method': 'SLSQP'    # or 'cvxpy'
}
