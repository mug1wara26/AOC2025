0
&fras"7"
⊜∘⊸≠@\n # Parse by new line
=@S°⊂   # create array of 0s except for start
˜⊙∘
Part₁ ← +/+≠0× # Count number of beams that hit splitters
# Get beams that hit splitters,
# rotate 1 and rotate -1,
# add together with beams that miss splitters
Part₂ ← ++⊃(⊃(↻1|↻¯1)×|×¬)
∧(⊃(Part₂|Part₁)=@^)
/+
