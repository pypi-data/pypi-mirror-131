class MyMethods:
    
    def sort_by(self, list, start_index, end_index, sort_value):
        # Get the middle index value if the starting index is lower than the end index
        if start_index < end_index:
            # Round the middle index value down if an even division is not possible
            middle_index = start_index + (end_index - start_index) // 2;
            # Sort data to the left and right of the index seperately
            self.sort_by(list, start_index, middle_index, sort_value)
            self.sort_by(list, middle_index + 1, end_index, sort_value)
            # Merge the sorted halves
            self.merge_sort_partitions(list, start_index, middle_index, end_index, sort_value)
    
    def merge_sort_partitions(self, list, start_index, middle_index, end_index, sort_value):
        # Determine the size of the arrays to be merged
        array_one_size = middle_index - start_index + 1
        array_two_size = end_index - middle_index

        # Create two temporary lists for adding values to
        temp_list_one = [] 
        temp_list_two = []
        
        
        
        # Pass values to the temp arrays using for loop to traverse list argument
        for index in range(array_one_size):
            temp_list_one.insert(index, list[start_index + index])
        for index in range(array_two_size):
            temp_list_two.insert(index, list[middle_index + index + 1])

        
        # Merge the temporary lists utilising variables below as index values
        i = 0
        j = 0
        k = start_index
        while i < array_one_size and j < array_two_size:
            if temp_list_one[i].get_sorting_filter(sort_value) <= temp_list_two[j].get_sorting_filter(sort_value):
                list[k] = temp_list_one[i]
                i+=1
            else:
                list[k] = temp_list_two[j]
                j+=1
            k+=1
        while i < array_one_size:
            list[k] = temp_list_one[i]
            i+=1
            k+=1
        while j < array_two_size:
            list[k] =  temp_list_two[j]
            j+=1
            k+=1