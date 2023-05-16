

function out = yesNo_data_remover(genre) 
for i = 1:size(genre,1)
    for j = 1:size(genre,2)
        if contains(genre(i,j),'Yes')
    genre(i,j) = 1;
        elseif contains(genre(i,j),'No')
    genre(i,j) = 0;
        end
    end
end
genre(1:2,:) = [];

    out = str2double(genre);
end
