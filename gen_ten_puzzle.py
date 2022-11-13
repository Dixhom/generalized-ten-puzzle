from itertools import permutations
from tqdm import tqdm

class GenTenPuzzle:
    """
    example: ten = GenTenPuzzle([1,1,5,8], 10).solve()
    """    
    def __init__(self, numbers, target, use_power=False, permutate=True, use_normal_operator_str=True):
        """This is a class to find the combinations of given numbers and operators to yield the number target
        for example, if the numbers are [8, 1, 1, 5] and the target is 10, the combination is 8 / (1 - 1 / 5) = 10

        Args:
            numbers (list[int]): numbers for calculation
            target (int): target for calculation
            use_power (bool, optional): use the power operator. Defaults to False.
            permutate (bool, optional): whether the numbers are permutated. Defaults to True.
            use_normal_operator_str (bool, optional): use normal operators like ÷ or × instead of / and *. Defaults to True.
        """
        self.numbers = numbers
        self.target = target
        self.operators = ['operand', self.__add, self.__subtract, self.__multiply, self.__divide]
        self.permutate = permutate
        self.use_normal_operator_str = use_normal_operator_str
        if use_power:
            self.operators += [self.__power]

    def __add(self, x, y): 
        """+""" 
        return x + y

    def __subtract(self, x, y): 
        """-"""
        return x - y

    def __multiply(self, x, y): 
        """*"""
        return x * y

    def __divide(self, x, y): 
        """/"""
        return x / y

    def __power(self, x, y): 
        """^"""
        return x ** y

    def __is_operand(self, n):
        """Whether n is an operand (numbers)

        Args:
            n (int): number

        Returns:
            bool: Whether n is an operand
        """        
        return isinstance(n, int) or isinstance(n, float)

    def __get_list_depth(self, l, depth=0):
        """get the depth of a list
        for example, "1" is depth 0. "[1, [2, 3, []]]" is depth 3.

        Args:
            l (list): list which the algorithm measure how deep is
            depth (int, optional): depth of the list. Defaults to 0.

        Returns:
            int: depth of the list
        """        
        if isinstance(l, list) and not l: # empty list
            return depth + 1

        current_depth = depth + 1
        max_depth = current_depth
        for elem in l:
            if isinstance(elem, list):
                ret_depth = self.__get_list_depth(elem, current_depth)
                if ret_depth > max_depth:
                    max_depth = ret_depth 
        return max_depth

    def __create_exprs_sub(self, created, rest, math_expr):
        """a subroutine for find the combination of numbers and operators to make the target.

        Args:
            created (list): numbers being created by operators
            rest (list): rest of the popped numbers
            math_expr (list)): created mathematical expression in reversed Polish notation

        Returns:
            list: list of mathematical expressions which make the target
        """        
        if not rest and len(created) == 1 and created[0] == self.target:
            return [math_expr] # return the final calculated result
        
        results = []
        for op in self.operators:
            created_cp = created[:]
            rest_cp = rest[:]
            math_expr_cp = math_expr[:]

            # __add a number
            if op == 'operand':
                if not rest_cp:
                    continue
                tmp = rest_cp.pop()
                created_cp.append(tmp)
                math_expr_cp.append(tmp)
                ret = self.__create_exprs_sub(created_cp, rest_cp, math_expr_cp)
                if not ret:
                    continue
                results += ret
                    
            # apply an operand
            else:
                if len(created_cp) < 2: # too few numbers for calculation
                    continue
                math_expr_cp.append(op.__doc__)
                n1 = created_cp.pop()
                n2 = created_cp.pop()
                if not self.__is_operand(n1) or not self.__is_operand(n2):
                    pass
                # zero division
                if op == self.__divide and n1 == 0:
                    continue
                created_cp.append(op(n2, n1)) # notice LIFO
                sub_op = self.__create_exprs_sub(created_cp, rest_cp, math_expr_cp)
                if not sub_op:
                    continue
                results += sub_op

        return results

    def __create_exprs(self, nums):
        """find the combination of numbers and operators to make the target.

        Args:
            nums (list): numbers for making the target

        Returns:
            list: list of mathematical expressions which make the target
        """        
        created = nums[:2] # the first 2 numbers are necessary so take them first
        rest = nums[2:][::-1] # reverse the rest for pop
        math_expr = created[:] # for math expression
        return self.__create_exprs_sub(created, rest, math_expr)
        
    def __polish_to_normal(self, polish):
        """turn a reserved Polish notation to a normal one

        Args:
            polish (list): a reserved Polish notation

        Raises:
            ValueError: there aren't enough numbers in the list

        Returns:
            str: a normal notation in string format
        """        
        polish = polish[::-1]
        stack = []
        while polish:
            p = polish.pop()
            if self.__is_operand(p):
                stack.append(p)
            elif len(stack) >= 2:
                n1 = stack.pop(); n2 = stack.pop()
                # replace the operator with one normally used in the society if necessary 
                if self.use_normal_operator_str:
                    if p == '*': p = '×'
                    elif p == '/': p = '÷'
                new_val = f'({n2} {p} {n1})'
                stack.append(new_val)
            else:
                print(polish, p, type(p), stack)
                raise ValueError(f'operator {p.__doc__} but there is only {len(stack)} value in the stack.')
        return stack[0]

    def solve(self):
        """"find the combination of numbers and operators to make the target.

        Returns:
            list: list of mathematical expressions which make the target
        """        
        num_list = set(permutations(self.numbers)) if self.permutate else [self.numbers]
        self.polish_list = []
        for n in tqdm(num_list):
            math_exprs = self.__create_exprs(list(n))
            if math_exprs:
                self.polish_list += math_exprs

        self.math_eq_list = [self.__polish_to_normal(m) for m in self.polish_list]
        return self.math_eq_list 
