#include <iostream>
#include <vector>
using namespace std;


int partition(vector<int>& nums, int low, int high){
    

    //partion function for quick sort algo to place all the elements less than the pivot to the left and and all of the elements greater to the right

    int pivot = nums[high];
    int i = low - 1;

    for (int j = low; j <high; ++j){
        if (nums[j] < pivot){
            ++i;
            swap(nums[i],nums[j]);
        }
    }
    swap(nums[i+1],nums[high]);
    return i + 1;

}

void quickSort(vector<int>& nums,int low, int high){
    
    //basic quicksort implementation partions the array then recursively calls each subset to sort it
    if (low < high){
        int pivot_idx = partition(nums,low,high);

        quickSort(nums,low, pivot_idx - 1);
        quickSort(nums,pivot_idx + 1, high);

    }
}


double sortAndFindMedian(vector<int>& nums){
    

    // given function to implement, just finds the median of the array
    quickSort(nums,0,nums.size() -1);

    int n = nums.size();
    if (n % 2 == 0){
        return (nums[n/2 - 1] + nums[n/2]) / 2.0;
    }

    else{
        return nums[n/2];
    }
}




int main(){

    cout << "Enter size of array: ";
    int size;
    cin >> size;

    vector<int> nums(size);
    cout << "Enter values for array seperated by spaces: ";
    for(int i = 0; i < size; ++i){
        cin >> nums[i];
    }

    double median = sortAndFindMedian(nums);
    cout << "The median is: " << median << endl;

    return 0;
}