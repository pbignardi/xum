devsetup:
	@uv sync

build: devsetup
	@uv run nuitka --onefile --output-file=xum --output-dir=build main.py 

install:
	@cp -f build/xum ~/.local/bin/xum

clean:
	@rm -rf main.bin
	@rm -rf main.dist
	@rm -rf build
	@rm -rf dist
