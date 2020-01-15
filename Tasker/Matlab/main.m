fileName = '3le.txt';
counter = 0;

fid = fopen(fileName); % open the file
id = "5";
while strlength(id)<5
    id = " " + id;
end

while ~feof(fid) % feof(fid) is true when the file ends
    line = fgetl(fid);
    
    if strlength(line)>50 && counter == 0
        display(line(3:7))
        display(id)
        counter = 1;
      if (counter == 0 && id == line(3:7))
          display(id == line(3:7))
          display(line(3:7))
          display(id)
      line1 = line % read one line
      end
    end
end
fclose(fid); % close the file
if(line1)
display(line1)
end
