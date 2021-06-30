# ccmus

simple python script for displaying album covers in cmus with tmux and ueberzug.

### usage
`python ccmus.py -h|-v`
<br>
- arguments determine orientation, horizontal or vertical, if left blank it will be determined automatically depending on terminal size.
- cover image should be saved as cover.jpg or cover.png 
- music directory path should be placed in `mu_path`
- albums should be stored in the following way:
<br>

```
  /mu-path
      /album_name
        /cover.jpg
```
- album_name should include cmus album_name returned from `cmus-remote -Q`
### dependencies
 `cmus` obviously
 <br>`tmux`
 <br>`ueberzug`
## examples

<img src="/examples/example_1.png" alt="example" width=450 height=330\>
<img src="/examples/example_3.png" alt="example" width=250 height=375\>

