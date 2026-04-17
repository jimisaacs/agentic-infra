package main

import (
	"encoding/json"
	"fmt"
	"os"

	"pulse/shared/pulse"

	"github.com/spf13/cobra"
)

func main() {
	root := &cobra.Command{
		Use:   "pulse",
		Short: "Lightweight health/status monitor",
	}

	check := &cobra.Command{
		Use:   "check [url]",
		Short: "Check the health of a URL",
		Args:  cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			result := pulse.Check(args[0])
			enc := json.NewEncoder(os.Stdout)
			enc.SetIndent("", "  ")
			return enc.Encode(result)
		},
	}

	root.AddCommand(check)

	if err := root.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
