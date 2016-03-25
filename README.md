# Html Assistant

## About:

Have you ever tried to write a simple website without php or rails help and got annoyed with copying and pasting header and navigation bar to all pages?

Html Assistant is a GUI program that saves your time with copying the same navigation/footer/header across all .html pages in specified folder.

## Example:
We have 10html files and we would like them to have the same code for navigation links. We can:

A) Open every file and paste our navigaton in each file. Every time we make additional change to our navigation we have to repeat this process.

B) Use Html Assistant

![alt text](https://github.com/GreatDanton/Html-Assistant-GUI/blob/master/screenshot.png "Html Assistant")

### Option B:


1.) Run Html Assistant

2.) Click on Open Project button (#1 on picture)

3.) Specify the element you would like to replace (#2 on picture). For example you would like to replace the following div:

```
 <div class="navigation">
	<ul>
		<li> First link </li>
		<li> Second link </li>
	</ul>
</div>
 ```
 
 so we type in the text field (#2 on picture):
 
 ```
<div class="navigation
 ```

4.) Files from the specified project (step 2) are automatically added into list view (#3 on picture)

5.) Write or paste new navigation in the text field below (#4 on picture) for example:

```
<div class="new_navigation">
	<ul>
		<li> Home </li>
		<li> About </li>
		<li> Contact </li>
	</ul>
</div>
```

6.) Press Update Navigation button (#5 on picture).

7.) See the changes in the console at the bottom of the window (#6 on picture).

8.) That's it. All 10 html files are now updated with the new navigation.


## Notes: 
Html Assistant is working fine if you are looking to replace <nav / <head / <footer <div **without** any div inside.

Nested divs should be working now, before you use Html Assistant on nested divs, make sure you have a backup of your files.


## Running Html Assistant:

In order to run this program you need python3 & gtk+ 3 installed on your computer.
