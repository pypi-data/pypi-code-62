class NextPermutation:
    def NextPermutation(self, nums: list) -> list:
        """
        :param nums: List of integers
      
        Given a word, find the lexicographically greater permutation of it.
        For example, lexicographically next permutation of “gfg” is “ggf” and next permutation of “acb” is “bac”.

        :return: Maximum sum subarray
        """
        found = False
        i = len(nums) - 2
        while i >= 0:
            if nums[i] < nums[i + 1]:
                found = True
                break
            i -= 1
        if not found:
            nums.sort()
        else:
            m = self.findMaxIndex(i + 1, nums, nums[i])
            nums[i], nums[m] = nums[m], nums[i]
            nums[i + 1:] = nums[i + 1:][::-1]
        return nums

    @staticmethod
    def findMaxIndex(index: int, a: list, curr: int) -> int:
        ans = -1
        # index = 0
        for i in range(index, len(a)):
            if a[i] > curr:
                if ans == -1:
                    ans = curr
                    index = i
                else:
                    ans = min(ans, a[i])
                    index = i
        return index
