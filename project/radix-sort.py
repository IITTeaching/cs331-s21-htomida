import urllib
import requests
import unittest

def book_to_words(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    booktxt = urllib.request.urlopen(book_url).read().decode()
    bookascii = booktxt.encode('ascii','replace')
    return bookascii.split()

def countingSort(arr, indx, maxl):
 
    n = len(arr)
 
    # Output array
    output = [0] * (n)
 
    # Build count array
    count = [0] * (256)
 
    # Store count of occurrences
    for i in range(0, n):
        pad = maxl - len(arr[i])
        if pad >= indx + 1:
            index = 0
            count[index] += 1
        else:
            index = int(arr[i][pad-(indx+1)])
            count[index] += 1
 
    # Change count array so it contains the position of string in output array
    for i in range(0, 256):
        count[i] += count[i - 1]
 
    # Build output array
    i = n - 1
    while i >= 0:
        # Adds padding to strings of length less than maxl
        pad = maxl - len(arr[i])
        if pad >= indx + 1:
            index = 0
        else:
            index = int(arr[i][pad-(indx+1)])
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        i -= 1
 
    # Copy output array to arr,
    i = 0
    for i in range(0, len(arr)):
        arr[i] = output[i]
 
# Radix sort
def radixSort(arr):
 
    sort = arr
    # Maximum length of string
    maxl = len(arr[0])
    for s in arr:
        if maxl < len(s):
            maxl = len(s)

    for i in range(maxl):
        countingSort(sort, i, maxl)
    
    return sort

def radix_a_book(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    words = book_to_words()
    return radixSort(words)

def test1():
    """Tests for sorting the whole book."""
    print(80 * "#" + "\nTest for sorting the whole book.")
    tc = unittest.TestCase()
    book_url='https://www.gutenberg.org/files/84/84-0.txt'
    booktxt = urllib.request.urlopen(book_url).read().decode()
    bookascii = booktxt.encode('ascii','replace')
    words = bookascii.split()
    radix_sort, regular_sort = radix_a_book(), sorted(words)
    test1_1(radix_sort, regular_sort)
    say_success()
    test1_2(radix_sort, regular_sort)
    say_success()
    test1_3(radix_sort, regular_sort)
    say_success()
    test1_4(radix_sort, regular_sort)
    say_success()
    test1_5(radix_sort, regular_sort)
    say_success()
    test1_6(radix_sort, regular_sort)
    say_success()

def test1_1(radix_sort, regular_sort):
    """Sort first 10 strings."""
    print("\t-sort first 10 strings")
    tc = unittest.TestCase()
    tc.assertEqual(radix_sort[:10], regular_sort[:10])
    
def test1_2(radix_sort, regular_sort):
    """Sort first 100 strings."""
    print("\t-sort first 100 strings")
    tc = unittest.TestCase()
    tc.assertEqual(radix_sort[:100], regular_sort[:100])

def test1_3(radix_sort, regular_sort):
    """Sort last 10 strings."""
    print("\t-sort last 10 strings")
    tc = unittest.TestCase()
    tc.assertEqual(radix_sort[-10:], regular_sort[-10:])

def test1_4(radix_sort, regular_sort):
    """Sort last 100 strings."""
    print("\t-sort last 100 strings")
    tc = unittest.TestCase()
    tc.assertEqual(radix_sort[-100:], regular_sort[-100:])

def test1_5(radix_sort, regular_sort):
    """Sort middle 100 strings."""
    print("\t-sort middle 100 strings")
    tc = unittest.TestCase()
    middle = len(radix_sort)//2
    tc.assertEqual(radix_sort[middle-50:middle+49], regular_sort[middle-50:middle+49])

def test1_6(radix_sort, regular_sort):
    """Sort whole book."""
    print("\t-sort whole book.")
    tc = unittest.TestCase()
    tc.assertTrue(radix_sort == regular_sort)
    #tc.assertEqual(radix_sort, regular_sort) #sometimes takes too much time

def say_success():
    print("\t\t----> SUCCESS")

def main():
    test1()
    print(80 * "#" + "\nALL TEST CASES FINISHED SUCCESSFULLY!\n" + 80 * "#")

if __name__ == '__main__':
    main()
